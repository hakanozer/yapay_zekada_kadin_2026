# Gemini ile Veri Analizi ve Sunumu — Proje Yapılacaklar Listesi

## Proje Özeti

Gemini Free API kullanarak kullanıcıların CSV, JSON veya Excel formatında veri seti yükleyip doğal dil ile analiz talebi girebildiği; sonuçların grafikler, tablolar ve özet bilgiler şeklinde sunulduğu tek sayfalık bir web uygulaması.

---

## Gemini API Kullanım Detayları
curl --location 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent' \
# --header 'x-goog-api-key: {API_KEY}' \
--header 'Content-Type: application/json' \
--data '{
    "contents": [
        {
            "parts": [
                {
                "text": "İstanbul fethi kaç yılındı oldu"
                }
            ]
        }
    ]
}

Gelen Yanıt:
{
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": "İstanbul'un fethi **1453** yılında gerçekleşmiştir. \n\nTam tarih **29 Mayıs 1453**'tür. Bu tarihi olay, Fatih Sultan Mehmet liderliğindeki Osmanlı ordusu tarafından gerçekleştirilmiştir.",
                        "thoughtSignature": "Eu0JCuoJAQw51seSzWh4q1qG..."
                    }
                ],
                "role": "model"
            },
            "finishReason": "STOP",
            "index": 0
        }
    ],
    "usageMetadata": {
        "promptTokenCount": 8,
        "candidatesTokenCount": 52,
        "totalTokenCount": 406,
        "promptTokensDetails": [
            {
                "modality": "TEXT",
                "tokenCount": 8
            }
        ],
        "thoughtsTokenCount": 346,
        "serviceTier": "standard"
    },
    "modelVersion": "gemini-3.5-flash",
    "responseId": "VtouapTLNfuakdUPhJqXuAc"
}


## Teknik Yığın

| Katman | Teknoloji |
|---|---|
| Backend | Python + FastAPI |
| Frontend | HTML + CSS + Vanilla JS (tek sayfa) |
| AI API | Google Gemini Free API |
| Grafikler | Chart.js |
| Tablolar | DataTables |
| Depolama | Tarayıcı localStorage (geçici, veritabanı yok) |
| Cache | Sunucu taraflı in-memory cache (dict tabanlı) |
| Konfigürasyon | `.env` dosyası (python-dotenv) |

---

## Proje Dosya Yapısı

```
gemini-veri-analizi/
├── main.py                  # FastAPI uygulaması giriş noktası
├── .env                     # GEMINI_API_KEY (git'e eklenmez)
├── .env.example             # Örnek env şablonu
├── requirements.txt
├── app/
│   ├── api/
│   │   └── routes.py        # API endpoint'leri
│   ├── services/
│   │   ├── gemini_service.py   # Gemini API iletişimi
│   │   ├── file_service.py     # Dosya parse ve validasyon
│   │   └── cache_service.py    # In-memory cache yönetimi
│   ├── models/
│   │   └── schemas.py       # Pydantic modeller (istek/yanıt şemaları)
│   └── core/
│       └── config.py        # Ayarlar ve sabitler
├── static/
│   ├── index.html           # Tek sayfa arayüz
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js           # Ana uygulama mantığı
│       ├── storage.js       # localStorage yönetimi
│       ├── charts.js        # Chart.js render
│       └── tables.js        # DataTables render
└── demo/
    └── demo_data.csv        # Demo veri seti
```

---

## Kurulum Gereksinimleri (`requirements.txt`)

```
fastapi
uvicorn[standard]
python-dotenv
google-generativeai
pandas
openpyxl
python-multipart
```

---

## Yapılacaklar Listesi

### 1. Proje Altyapısı

- [ ] Proje klasör yapısını oluştur
- [ ] `requirements.txt` dosyasını oluştur ve bağımlılıkları kur
- [ ] `.env` ve `.env.example` dosyalarını oluştur (`GEMINI_API_KEY` ve `MAX_FILE_SIZE_KB=500`)
- [ ] FastAPI uygulamasını başlat (`main.py`), static dosyaları ve HTML'i servis edecek şekilde yapılandır
- [ ] OOP ve SOLID prensiplerine uygun modüler klasör yapısı kur

### 2. Backend — Dosya Yükleme ve Validasyon

- [ ] `file_service.py` — Dosya parse ve validasyon sınıfı yaz:
  - [ ] Desteklenen formatlar: `.csv`, `.json`, `.xlsx`, `.xls`
  - [ ] Maksimum dosya boyutu: 500 KB kontrolü (aşılırsa `400` hatası)
  - [ ] Dosya içeriğini pandas DataFrame'e dönüştür
  - [ ] Veri önizleme: İlk 5 satırı ve kolon adlarını döndür
- [ ] `POST /api/upload` endpoint'ini yaz — dosya yükle, önizleme döndür

### 3. Backend — Gemini API Entegrasyonu

- [ ] `gemini_service.py` — Gemini API servis sınıfı yaz:
  - [ ] `GEMINI_API_KEY`'i `.env` üzerinden yükle
  - [ ] System prompt: AI'yi yalnızca veri analizi uzmanı rolünde tut, chatbot kullanımını engelle
  - [ ] Kullanıcı isteğini ve veri setini Gemini'ye gönder
  - [ ] Yanıtı zorunlu olarak JSON formatında döndürmesini iste (prompt'ta belirt)
  - [ ] JSON parse hatasında anlamlı hata mesajı döndür
  - [ ] Gemini API kota/rate limit hatalarını yakala ve kullanıcıya uygun mesaj göster
- [ ] `POST /api/analyze` endpoint'ini yaz:
  - [ ] Analiz metni boş gelirse `422` hatası döndür (Gemini'ye gitme)
  - [ ] Dosya yüklenmeden analiz isteği gelirse `400` hatası döndür
  - [ ] Sonuca `requested_at` (ISO 8601) zaman damgası ekle

### 4. Backend — Cache Yönetimi

- [ ] `cache_service.py` — In-memory cache sınıfı yaz:
  - [ ] Cache anahtarı: `hash(dosya_içeriği + analiz_metni)`
  - [ ] Aynı veri seti + aynı analiz metni kombinasyonu için önbellek kontrolü yap
  - [ ] Cache'te bulunursa Gemini'ye istek atmadan önbellekten döndür
  - [ ] Cache boyutunu sınırla (maksimum 50 kayıt, FIFO temizleme)

### 5. Backend — API Endpoint Özeti

| Method | Path | Açıklama |
|---|---|---|
| `POST` | `/api/upload` | Dosya yükle, önizleme döndür |
| `POST` | `/api/analyze` | Analiz isteği gönder, JSON sonuç al |
| `GET` | `/api/demo` | Demo veri seti ve örnek analiz sonucu döndür |
| `GET` | `/` | Frontend HTML sayfasını servis et |

Tüm endpoint'ler JSON formatında yanıt döndürür.

### 6. Frontend — Sayfa Yapısı ve Layout

- [ ] Tek sayfa HTML tasarımı yap — iki sütunlu layout:
  - **Sol panel (1/3 genişlik):** Geçmiş analizler listesi
  - **Sağ panel (2/3 genişlik):** Yeni analiz formu veya seçili analizin detayları
- [ ] Sol panelde her analiz kaydında şunlar gösterilmeli:
  - Dosya adı
  - Analiz talebinin kısa özeti (ilk 60 karakter)
  - Analiz tarihi ve saati
  - Sil butonu
- [ ] Kullanıcı sol panelden bir analiz seçtiğinde, sağ panel o analizin görselleştirilmiş sonuçlarını göstermeli
- [ ] Responsive tasarım: Mobilde tek sütun, geçmiş analizler üstte/daraltılmış

### 7. Frontend — Yeni Analiz Formu

- [ ] Dosya yükleme alanı:
  - [ ] Sürükle-bırak ve klasik dosya seçimi desteği
  - [ ] Yükleme sırasında dosya boyutu 500 KB kontrolü (frontend tarafında da yapılsın)
  - [ ] 500 KB aşılırsa kullanıcıya uyarı göster, Gemini'ye istek gönderme
  - [ ] Yükleme başarılıysa veri önizlemesini göster (kolon adları + ilk 5 satır)
- [ ] Analiz talebi metin alanı:
  - [ ] Boş bırakılırsa analiz butonu devre dışı / gönderimde uyarı göster
  - [ ] Placeholder: "Bu veri setinden ne analiz etmek istiyorsunuz? (örn: aylık satış trendini göster)"
- [ ] "Analiz Et" butonu — yükleme ve analiz aşamalarında spinner göster
- [ ] "Demo Veri Setini Yükle" butonu — kullanıcıyı sistemi önceden denemesi için yönlendir

### 8. Frontend — Sonuç Görselleştirme

- [ ] Analiz sonucu JSON döndüğünde şu bölümleri render et:
  - [ ] **Özet bilgi kartları** — temel metrikler (örn. toplam satış, ortalama, en yüksek değer)
  - [ ] **Grafikler** — Chart.js ile (bar, line, pie — Gemini'nin JSON'undaki grafik tipine göre)
  - [ ] **Veri tablosu** — DataTables ile (arama, sıralama, sayfalama destekli)
- [ ] Analiz tarihi ve saatini sonuç alanında göster
- [ ] Sonuç bölümünde eylem butonları:
  - [ ] **JSON'u Kopyala** — panoya kopyala
  - [ ] **JSON İndir** — `.json` dosyası olarak indir
  - [ ] **Paylaş** — analiz sonucunu JSON dosyası olarak dışa aktar (localStorage tabanlı mimaride URL paylaşımı mümkün olmadığından export yöntemi kullanılır)

### 9. Frontend — localStorage Yönetimi

- [ ] `storage.js` — localStorage sınıfı yaz:
  - [ ] Analiz kaydını kaydet: `{ id, fileName, prompt, result, createdAt }`
  - [ ] Tüm kayıtları listele
  - [ ] Belirli kaydı sil
  - [ ] Tüm kayıtları temizle
  - [ ] localStorage doluluk kontrolü — dolu olursa eski kaydı sil ve kullanıcıyı bilgilendir

### 10. Frontend — Tema

- [ ] Açık / koyu mod toggle butonu ekle (header'da)
- [ ] Tercih `localStorage`'a kaydet ve sayfa yenilenmesinde hatırla
- [ ] CSS custom properties (`--color-*`) kullanarak iki tema arasında geçiş yap
- [ ] Sistem temasını (`prefers-color-scheme`) varsayılan olarak algıla

### 11. Hata Yönetimi

- [ ] Frontend: Her API hatasında kullanıcıya toast/banner ile anlamlı mesaj göster
- [ ] Backend: Tüm exception'lar için standart JSON hata yapısı döndür: `{ "error": true, "message": "..." }`
- [ ] Yakalanması gereken hata senaryoları:
  - [ ] Dosya boyutu aşımı (frontend + backend)
  - [ ] Desteklenmeyen dosya formatı
  - [ ] Analiz metni boş
  - [ ] Gemini API kota/rate limit hatası
  - [ ] Gemini yanıtı geçerli JSON değil
  - [ ] localStorage doluluk hatası

### 12. Demo Modu

- [ ] `demo/demo_data.csv` — örnek sipariş verisi oluştur (en az 20 satır, ürün/tarih/miktar/fiyat kolonları)
- [ ] `GET /api/demo` endpoint'i — demo dosyayı yükleyip örnek bir analiz sonucu döndürsün
- [ ] Frontend'de "Demo ile Dene" butonu — tek tıkla demo veri setini yükleyip önizleme göstersin

### 13. Güvenlik ve Kısıtlar

- [ ] Gemini API key sunucu tarafında tutulur, frontend'e asla iletilmez
- [ ] Sistem promptu kullanıcıya gösterilmez, backend'de sabit kodlanır
- [ ] Kullanıcı Gemini API'yi yalnızca veri analizi için kullanabilir; chatbot veya genel sohbet talebi system prompt ile engellenir
- [ ] Yüklenen dosyalar sunucuda kalıcı olarak saklanmaz; işlem sonrası bellekten temizlenir

---

## Kapsam Dışı (Bu Projede Yapılmayacaklar)

- Kullanıcı kimlik doğrulaması / oturum yönetimi
- Veritabanı entegrasyonu
- Gerçek zamanlı URL tabanlı paylaşım (localStorage kısıtı nedeniyle)
- 500 KB üzeri dosya desteği
- Gemini dışında başka AI modeli desteği
