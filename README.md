# 🍽️ AI Yemek Öneri Uygulaması

Ollama ile çalışan, tamamen lokal ve ücretsiz AI yemek öneri sitesi.

## Proje Yapısı

```
yemek_oneri/
├── app.py              # Ana giriş noktası
├── config.py           # Tüm ayarlar
├── ai/
│   ├── client.py       # Ollama bağlantısı
│   └── prompts.py      # AI prompt şablonları
├── routes/
│   └── handler.py      # HTTP istek yöneticisi
├── templates/
│   └── index.html      # HTML arayüzü
└── static/
    ├── style.css        # Stiller
    └── app.js           # JavaScript
```

## Kurulum

```bash
# 1. Ollama indir
# https://ollama.com/download

# 2. Modeli indir (bir kez)
ollama pull llama3.2

# 3. Uygulamayı başlat
python app.py

# 4. Tarayıcıda aç
# http://localhost:8765
```

## Özellikler

- 🤖 Tamamen lokal AI (internet yok, ücretsiz)
- 🍽️ Öğün / diyet / mutfak tercihine göre öneri
- 🧑‍🍳 Eldeki malzemelere göre tarif bulma
- 🔥 Kalori ve besin değerleri
- 📱 Responsive tasarım
