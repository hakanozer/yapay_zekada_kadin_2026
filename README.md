# Makale Arama — Gemini Destekli Akademik Araştırma

Google Gemini 2.0 Flash API'si ile güçlendirilmiş, hakemli akademik makaleleri arayıp anında özetleyen bir web uygulaması. PubMed, arXiv, IEEE Xplore, Nature ve daha fazlasından sonuçlar getirir.

---

## Kurulum

### 1. Sanal Ortam Oluşturma

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows
```

### 2. Bağımlılıkları Kurma

```bash
pip install -r requirements.txt
pip install -q -U google-genai
```

### 3. `.env` Dosyasını Ayarlama

Proje kökünde `.env` dosyası oluşturun:

```env
GEMINI_API_KEY=your_api_key_here
```

> **Uyarı:** `.env` dosyasını asla Git'e commit'lemeyin. `.gitignore` zaten bunu engeller.

---

## Çalıştırma

```bash
uvicorn makale_arama_projesi.main:app --reload --host 0.0.0.0 --port 8000
```

Uygulama şu adreste açılır: [http://localhost:8000](http://localhost:8000)

---

## Endpoint Listesi

| Method | Path | Açıklama |
|--------|------|----------|
| `GET` | `/` | Ana sayfa HTML |
| `GET` | `/api/health` | Sistem sağlık kontrolü |
| `POST` | `/api/search` | Makale arama |
| `POST` | `/api/summarize` | Makale özetleme |

### Örnek: Makale Arama

**İstek:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "kadınlar yapay zeka", "language": "tr"}'
```

**Yanıt:**
```json
{
  "query": "kadınlar yapay zeka",
  "results": [
    {
      "title": "Women in Artificial Intelligence: Challenges and Opportunities",
      "authors": "Smith J., Doe A.",
      "year": "2023",
      "source": "Nature Machine Intelligence",
      "abstract": "Bu çalışma...",
      "doi": "10.1038/s42256-023-00001-1",
      "url": null,
      "relevance_score": 0.96
    }
  ],
  "total_count": 8,
  "search_duration_ms": 4231.5
}
```

### Örnek: Makale Özetleme

**İstek:**
```bash
curl -X POST http://localhost:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"title": "Women in AI", "abstract": "Bu makale...", "doi": "10.1038/..."}'
```

**Yanıt:**
```json
{
  "summary": "Makale, yapay zeka alanında cinsiyet eşitsizliğini...",
  "key_points": ["Kadınlar YZ araştırmacılarının %18'ini oluşturuyor", "..."],
  "methodology": "Meta-analiz ve literatür taraması",
  "findings": "Kurumsal destek artırıldığında katılım oranı yükselmektedir."
}
```

---

## Dizin Yapısı

```
proje_kök/
├── venv/                          # Python sanal ortamı (git'e dahil edilmez)
├── .env                           # Ortam değişkenleri (git'e dahil edilmez)
├── .gitignore
├── requirements.txt
├── README.md
└── makale_arama_projesi/
    ├── __init__.py
    ├── main.py                    # FastAPI uygulamasının giriş noktası
    ├── config.py                  # Ayarlar ve ortam değişkenleri
    ├── gemini_client.py           # Gemini API istemcisi ve iş mantığı
    ├── models.py                  # Pydantic request/response şemaları
    ├── cache.py                   # In-memory cache katmanı (TTL destekli)
    └── templates/
        └── index.html             # Tek sayfalık kullanıcı arayüzü
```
