"""
Uygulama ayarları.
Tüm sabitler buradan yönetilir.
"""

import os

# ── Sunucu ────────────────────────────────────────────────────────────────────
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8765))

# ── Ollama ────────────────────────────────────────────────────────────────────
OLLAMA_URL     = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL   = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_TIMEOUT = 120   # saniye

# ── AI Parametreleri ──────────────────────────────────────────────────────────
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS  = 1500

# ── Uygulama ──────────────────────────────────────────────────────────────────
APP_NAME    = "AI Yemek Öneri"
APP_VERSION = "1.0.0"