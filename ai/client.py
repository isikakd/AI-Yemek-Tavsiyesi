"""
Ollama API istemcisi.
Tüm AI iletişimi bu modül üzerinden geçer.
"""

import json
import re
import urllib.request
import urllib.error

from config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT, AI_TEMPERATURE


class OllamaClient:
    """Ollama lokal AI sunucusu ile iletişim kurar."""

    def __init__(self, url: str = OLLAMA_URL, model: str = OLLAMA_MODEL):
        self.url   = url
        self.model = model

    def chat(self, prompt: str) -> str:
        """
        Verilen prompt'u Ollama'ya gönderir, yanıt metnini döner.
        Raises:
            urllib.error.URLError  - Ollama çalışmıyorsa
            ValueError             - Boş yanıt gelirse
        """
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": AI_TEMPERATURE}
        }).encode()

        req = urllib.request.Request(
            self.url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            data = json.loads(resp.read())

        content = data.get("message", {}).get("content", "").strip()
        if not content:
            raise ValueError("Ollama boş yanıt döndürdü.")
        return content

    def chat_json(self, prompt: str) -> dict:
        """
        Yanıtı JSON olarak parse eder.
        Raises:
            json.JSONDecodeError - Geçersiz JSON gelirse
        """
        raw   = self.chat(prompt)
        clean = re.sub(r"^```[a-z]*\n?", "", raw.strip())
        clean = re.sub(r"```$", "", clean).strip()
        return json.loads(clean)

    def is_available(self) -> bool:
        """Ollama sunucusunun çalışıp çalışmadığını kontrol eder."""
        try:
            req = urllib.request.Request(
                self.url.replace("/api/chat", "/api/tags"),
                method="GET"
            )
            urllib.request.urlopen(req, timeout=3)
            return True
        except Exception:
            return False
