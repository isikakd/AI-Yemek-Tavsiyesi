"""
AI prompt şablonları.
Tüm prompt metinleri buradan yönetilir.
"""

JSON_RECIPE_SCHEMA = """
{
  "yemekler": [
    {
      "isim": "Yemek Adı",
      "emoji": "🍽️",
      "kalori": 350,
      "sure": "30 dk",
      "zorluk": "Kolay",
      "malzemeler": ["malzeme1", "malzeme2", "malzeme3"],
      "tarif": "Adım adım kısa tarif açıklaması (3-4 cümle).",
      "besin": {"protein": "20g", "karbonhidrat": "45g", "yag": "12g"},
      "etiketler": ["Sağlıklı", "Hızlı"]
    }
  ]
}"""


class PromptBuilder:
    """Farklı senaryolar için prompt metni üretir."""

    @staticmethod
    def suggest(meal: str, diet: str, cuisine: str) -> str:
        """Öğün, diyet ve mutfak tercihine göre yemek önerisi promptu."""
        return f"""Sen uzman bir aşçı ve beslenme danışmanısın.
Aşağıdaki tercihlere göre 4 farklı yemek öner.

Tercihler:
- Öğün: {meal}
- Diyet: {diet}
- Mutfak: {cuisine}

SADECE aşağıdaki JSON formatında cevap ver, başka hiçbir şey yazma:
{JSON_RECIPE_SCHEMA}

Kurallar:
- Türkçe yaz
- Kalorileri gerçekçi tut
- Emojileri yemeğe uygun seç
- Zorluk: Kolay / Orta / Zor"""

    @staticmethod
    def fridge(ingredients_text: str) -> str:
        """Eldeki malzemelere göre tarif önerisi promptu."""
        return f"""Sen uzman bir aşçısın.
Kullanıcının elindeki malzemelere göre yemek önerileri sun.

Kullanıcının mesajı: "{ingredients_text}"

Bu malzemelerle yapılabilecek 3 farklı yemek öner.
SADECE aşağıdaki JSON formatında cevap ver, başka hiçbir şey yazma:
{JSON_RECIPE_SCHEMA}

Kurallar:
- Türkçe yaz
- Kullanıcının bahsettiği malzemeleri mutlaka kullan
- Pratik ve yapımı kolay tarifler seç"""
