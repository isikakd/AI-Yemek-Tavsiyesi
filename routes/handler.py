"""
HTTP istek yöneticisi.
Gelen istekleri ilgili servislere yönlendirir.
"""

import json
import os
import traceback
import urllib.error
from http.server import BaseHTTPRequestHandler

from ai import OllamaClient, PromptBuilder

# Singleton AI client
_client = OllamaClient()


class RequestHandler(BaseHTTPRequestHandler):
    """Tüm HTTP isteklerini karşılar."""

    # ── Loglama ───────────────────────────────────────────────────────────────
    def log_message(self, fmt, *args):
        method = args[0] if args else "?"
        status = args[1] if len(args) > 1 else "?"
        print(f"  [{method}] {status}")

    # ── GET ───────────────────────────────────────────────────────────────────
    def do_GET(self):
        path = self.path.split("?")[0]

        if path == "/" or path == "/index.html":
            self._serve_file("templates/index.html", "text/html")
        elif path == "/static/style.css":
            self._serve_file("static/style.css", "text/css")
        elif path == "/static/app.js":
            self._serve_file("static/app.js", "application/javascript")
        elif path == "/api/health":
            self._json({"status": "ok", "ollama": _client.is_available()})
        else:
            self._json({"error": "Sayfa bulunamadı"}, 404)

    # ── POST ──────────────────────────────────────────────────────────────────
    def do_POST(self):
        path = self.path.split("?")[0]

        try:
            body = self._read_body()

            if path == "/api/suggest":
                result = self._handle_suggest(body)
            elif path == "/api/fridge":
                result = self._handle_fridge(body)
            else:
                self._json({"error": "Bilinmeyen endpoint"}, 404)
                return

            self._json(result)

        except urllib.error.URLError:
            msg = ("Ollama'ya bağlanılamadı. "
                   "Terminalde 'ollama serve' çalıştırın.")
            print(f"  [HATA] {msg}")
            self._json({"error": msg}, 503)

        except json.JSONDecodeError as e:
            print(f"  [JSON HATA] {e}")
            self._json({"error": "AI yanıtı çözümlenemedi, tekrar deneyin."}, 500)

        except Exception as e:
            print(f"  [GENEL HATA]\n{traceback.format_exc()}")
            self._json({"error": str(e)}, 500)

    # ── Özel route metodları ──────────────────────────────────────────────────
    def _handle_suggest(self, body: dict) -> dict:
        meal    = body.get("meal", "Akşam Yemeği")
        diet    = body.get("diet", "Hepsi")
        cuisine = body.get("cuisine", "Her İkisi")
        prompt  = PromptBuilder.suggest(meal, diet, cuisine)
        return _client.chat_json(prompt)

    def _handle_fridge(self, body: dict) -> dict:
        text   = body.get("text", "").strip()
        if not text:
            raise ValueError("Malzeme metni boş olamaz.")
        prompt = PromptBuilder.fridge(text)
        return _client.chat_json(prompt)

    # ── Yardımcı metodlar ─────────────────────────────────────────────────────
    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length))

    def _serve_file(self, filepath: str, content_type: str):
        # app.py'nin bulunduğu kök dizini baz al
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full = os.path.join(base, filepath)
        print(f"  [STATIC] {full}")
        try:
            with open(full, "rb") as fh:
                data = fh.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            print(f"  [404] Dosya bulunamadı: {full}")
            self._json({"error": f"{filepath} bulunamadı"}, 404)

    def _json(self, data: dict, code: int = 200):
        payload = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(payload))
        self.end_headers()
        self.wfile.write(payload)
