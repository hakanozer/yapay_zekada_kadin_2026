# projeyi çalıştırma: uvicorn makale_arama_projesi.main:app --reload --host 0.0.0.0 --port 8000

# Makale Arama Projesi — Task Specification

## Proje Genel Bakış

Gemini API kullanılarak geliştirilecek, akademik makale arama ve özetleme işlemlerini gerçekleştiren web uygulaması. Backend FastAPI, frontend tek sayfalık Bootstrap HTML, API katmanı Google Gemini ile sağlanacak.

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
    ├── main.py                    # Uygulamanın giriş noktası
    ├── config.py                  # Ayarlar ve ortam değişkenleri
    ├── gemini_client.py           # Gemini API istemcisi ve iş mantığı
    ├── models.py                  # Pydantic request/response şemaları
    ├── cache.py                   # In-memory cache katmanı
    └── templates/
        └── index.html             # Tek sayfalık kullanıcı arayüzü
```

---

## Bağımlılıklar

`requirements.txt` içeriği:

```
fastapi
uvicorn[standard]
google-genai
jinja2
python-multipart
python-dotenv
```

Kurulum komutu: `pip install -r requirements.txt`
google-genai ek kurulum: `pip install -q -U google-genai`

---

## Ortam Değişkenleri

`.env` dosyası (asla git'e commit'lenmez):

```
GEMINI_API_KEY=AIzaSyBw8UhHH39jYNcETvyNhmVuTfeQeHWARcM
```

`.gitignore` içeriği:

```
venv/
.env
__pycache__/
*.pyc
.DS_Store
```

---

## Modüller ve Sorumluluklar

### `config.py`
- `python-dotenv` ile `.env` dosyasını yükler
- `GEMINI_API_KEY` ortam değişkenini okur, yoksa uygulama başlatma hatası fırlatır
- Uygulama genelinde kullanılacak sabitler (model adı, max token, cache TTL süresi vb.) burada tanımlanır
- Kullanılacak Gemini modeli: `gemini-2.0-flash`

### `models.py`
Pydantic ile tanımlanacak veri şemaları:

| Model | Alanlar | Açıklama |
|---|---|---|
| `SearchRequest` | `query: str`, `language: str = "tr"` | Arama isteği |
| `ArticleResult` | `title`, `authors`, `year`, `source`, `abstract`, `doi`, `url`, `relevance_score` | Tek makale sonucu |
| `SearchResponse` | `query`, `results: list[ArticleResult]`, `total_count`, `search_duration_ms` | Arama yanıtı |
| `SummarizeRequest` | `title`, `abstract`, `doi` | Özetleme isteği |
| `SummarizeResponse` | `summary`, `key_points: list[str]`, `methodology`, `findings` | Özetleme yanıtı |
| `ErrorResponse` | `error_code`, `message`, `detail` | Hata yanıtı |

Tüm string alanlar için validator ile boş string kontrolü yapılır.
`query` alanı minimum 3, maksimum 500 karakter olarak kısıtlanır.

### `cache.py`
- Python `dict` tabanlı in-memory cache
- Her cache girdisi için TTL (Time-To-Live) desteği — varsayılan 10 dakika
- Arama sonuçları ve özetler ayrı ayrı cache'lenir
- Cache key: query string'in SHA-256 hash'i
- `get(key)`, `set(key, value)`, `invalidate(key)`, `clear()` metotları
- Uygulama başlatıldığında cache sıfırdan oluşturulur, uygulama durduğunda tüm veri kaybolur (kalıcı depolama yok)

### `gemini_client.py`
`google-genai` kütüphanesiyle Gemini API bağlantısı.

**`search_articles(query: str, language: str) -> list[ArticleResult]`**

Sistem prompt'u şu kriterleri içerir:
- Yalnızca hakemli (peer-reviewed) akademik makaleler döndür
- Güvenilir kaynaklar: PubMed, arXiv, IEEE Xplore, Springer, Elsevier, Nature, Science, JSTOR
- Her sonuç için başlık, yazarlar, yayın yılı, kaynak/dergi, kısa abstract, DOI veya URL içermeli
- Sonuçlar alaka düzeyine göre sırala
- Kullanıcının dil tercihine göre yanıt döndür
- Maksimum 10 sonuç döndür
- Yanıtı JSON formatında üret (structured output)

Grounding özelliği (`tools=[Tool(google_search=GoogleSearch())]`) aktif edilir, böylece Gemini güncel akademik veritabanlarını tarayabilir.

**`summarize_article(title: str, abstract: str) -> SummarizeResponse`**

Sistem prompt'u şu kriterleri içerir:
- Makalenin ana argümanını 2-3 cümleyle özetle
- Kullanılan metodoloji nedir?
- Temel bulgular ve sonuçlar nelerdir?
- 3-5 madde halinde anahtar çıkarımlar listele
- Akademik olmayan okuyucu için sade dil kullan
- Gereksiz tekrar ve jargon içerme
- Yanıtı JSON formatında üret

Her iki fonksiyon da `async` olarak tanımlanır, hata durumunda `HTTPException` fırlatır.

### `main.py`
FastAPI uygulamasının ana dosyası.

**Uygulama Kurulumu:**
- `FastAPI` örneği oluşturulur, `title`, `description`, `version` metadata'sı eklenir
- `CORSMiddleware` eklenir:
  - `allow_origins`: geliştirme için `["*"]`, üretim için yalnızca izin verilen domain'ler
  - `allow_methods`: `["GET", "POST"]`
  - `allow_headers`: `["*"]`
- `Jinja2Templates` ile `templates/` dizini bağlanır
- `StaticFiles` gerekirse bağlanır

**Endpointler:**

| Method | Path | Açıklama | Request | Response |
|---|---|---|---|---|
| `GET` | `/` | Ana sayfa HTML döndürür | — | `HTMLResponse` |
| `POST` | `/api/search` | Makale arama | `SearchRequest` | `SearchResponse` |
| `POST` | `/api/summarize` | Makale özetleme | `SummarizeRequest` | `SummarizeResponse` |
| `GET` | `/api/health` | Sistem sağlık kontrolü | — | `{"status": "ok"}` |

**Global Hata Yönetimi:**
- `@app.exception_handler(HTTPException)`: HTTP hatalarını yakalar, `ErrorResponse` döndürür
- `@app.exception_handler(Exception)`: Beklenmeyen tüm hataları yakalar, 500 döndürür, hata loglanır
- `@app.exception_handler(RequestValidationError)`: Pydantic validasyon hatalarını yakalar, 422 döndürür, hangi alan hatalı olduğunu belirtir

**Startup/Shutdown:**
- `@app.on_event("startup")`: Gemini istemcisi başlatılır, config doğrulanır
- `@app.on_event("shutdown")`: Cache temizlenir

**Çalıştırma:**
```bash
uvicorn makale_arama_projesi.main:app --reload --host 0.0.0.0 --port 8000
```

---

## `templates/index.html` — Arayüz Gereksinimleri

**Genel:**
- Tek dosya HTML (CSS ve JS aynı dosyada)
- Bootstrap 5 CDN ile yüklenir
- Türkçe dil desteği (`lang="tr"`)
- Responsive tasarım, mobil uyumlu

**Bileşenler:**

**1. Navbar**
- Uygulama adı ve kısa açıklama
- Sağ üstte GitHub linki (opsiyonel)

**2. Arama Formu**
- Geniş metin alanı (arama sorgusu)
- "Makale Ara" butonu
- Form submit'te `fetch()` ile `/api/search` POST isteği gönderilir
- İstek sırasında buton disable, spinner gösterilir
- Minimum 3 karakter validasyonu frontend'de de yapılır

**3. Sonuç Alanı**
- Arama yapılmadan önce boş, yönlendirici bir placeholder gösterilir
- Her makale için Bootstrap card bileşeni:
  - Başlık (bold)
  - Yazarlar ve yayın yılı (muted text)
  - Kaynak/dergi adı (badge)
  - Abstract (ilk 300 karakter, "Devamını gör" toggle'ı)
  - DOI / Kaynak linki (yeni sekmede açılır)
  - "Özetle" butonu — tıklandığında `/api/summarize` POST isteği gönderilir
- Sonuç sayısı ve arama süresi gösterilir

**4. Özetleme Modalı (Bootstrap Modal)**
- "Özetle" butonuna basılınca açılır
- Modal içinde spinner gösterilir, sonuç gelince:
  - Genel özet
  - Metodoloji
  - Temel bulgular
  - Anahtar çıkarımlar (madde madde)
- "Kopyala" butonu: tüm özeti panoya kopyalar

**5. Hata Gösterimi**
- API'dan hata geldiğinde Bootstrap `alert alert-danger` ile kullanıcıya gösterilir
- Hata mesajı kapatılabilir (dismiss butonu)
- Ağ hatası ile API hatası ayrı mesajlarla gösterilir

**6. Loading Durumları**
- Arama sırasında: buton disabled + spinner
- Özetleme sırasında: modal içinde spinner
- Yükleme tamamlanınca spinner gizlenir

**JavaScript Gereksinimleri:**
- Vanilla JS (framework yok)
- `async/await` ile `fetch()` API çağrıları
- DOM manipülasyonu ile dinamik kart oluşturma
- Hata durumlarında try/catch

---

## Akış Diyagramı

```
Kullanıcı → Arama Formu
    ↓
POST /api/search
    ↓
Cache kontrol (hit → anında dön)
    ↓ (miss)
gemini_client.search_articles()
    ↓
Gemini API (grounding aktif)
    ↓
ArticleResult listesi parse
    ↓
Cache'e yaz (10 dk TTL)
    ↓
SearchResponse → Arayüz

Kullanıcı → "Özetle" butonu
    ↓
POST /api/summarize
    ↓
Cache kontrol (DOI hash'i ile)
    ↓ (miss)
gemini_client.summarize_article()
    ↓
SummarizeResponse → Modal
```

---

## Kısıtlamalar ve Kurallar

- Veritabanı kullanılmaz; tüm veri geçici (in-memory)
- Arama sonuçları yalnızca hakemli akademik kaynaklardan gelir
- Arayüzde akademik sonuçlar dışında bilgi gösterilmez
- API anahtarı asla frontend'e gönderilmez, asla kaynak kodda açık yazılmaz
- Her iki endpoint için istek başına timeout: 30 saniye
- Gemini'den JSON dışı yanıt gelirse parse hatası yakalanır, kullanıcıya anlamlı hata gösterilir
- CORS sadece gerekli origin'lere açılır; üretimde `allow_origins=["*"]` kullanılmaz

---


## README.md İçeriği

README şu bölümleri içerir:

1. Proje açıklaması (2-3 cümle)
2. Kurulum adımları (venv oluşturma → bağımlılık kurma → `.env` ayarlama)
3. Çalıştırma komutu
4. Endpoint listesi ve örnek istek/yanıt
5. Dizin yapısı açıklaması
