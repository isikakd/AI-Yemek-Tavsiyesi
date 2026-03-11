#!/usr/bin/env python3
"""
🍽️  AI Yemek Öneri Uygulaması
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Çalıştır : python app.py
Tarayıcı : http://localhost:8765

Gereksinim:
  - Ollama kurulu olmalı  → https://ollama.com/download
  - Model indirilmeli     → ollama pull llama3.2
"""

import os
import socket
from http.server import HTTPServer

# Proje kök dizinini Python path'e ekle ve oraya geç
import sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)  # Statik dosyalar için çalışma dizinini ayarla

from config import HOST, PORT, APP_NAME, APP_VERSION, OLLAMA_MODEL
from routes import RequestHandler
from ai import OllamaClient


def check_ollama():
    """Ollama'nın çalışıp çalışmadığını kontrol eder."""
    client = OllamaClient()
    if not client.is_available():
        print("\n  ⚠️  UYARI: Ollama çalışmıyor!")
        print("  Yeni bir terminal açıp şunu çalıştırın:")
        print("    ollama serve")
        print(f"  Model hazır mı kontrol edin:")
        print(f"    ollama pull {OLLAMA_MODEL}\n")
        return False
    return True


def run():
    server = HTTPServer((HOST, PORT), RequestHandler)
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("=" * 50)
    print(f"  🍽️  {APP_NAME} v{APP_VERSION}")
    print("=" * 50)

    ollama_ok = check_ollama()
    status = "✅ Hazır" if ollama_ok else "⚠️  Ollama bekleniyor"
    print(f"  Ollama : {status}")
    print(f"  Model  : {OLLAMA_MODEL}")
    print(f"  🌐  http://localhost:{PORT}")
    print("  🛑  Durdurmak için Ctrl+C")
    print("=" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Uygulama kapatıldı. Görüşürüz! 👋")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
