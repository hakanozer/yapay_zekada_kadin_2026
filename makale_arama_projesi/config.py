"""
config.py — Uygulama ayarları ve ortam değişkenleri
"""

import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Gemini API Anahtarı
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY ortam değişkeni bulunamadı. "
        "Lütfen .env dosyasını oluşturun ve GEMINI_API_KEY değerini ekleyin."
    )

# Model ayarları
GEMINI_MODEL: str = "gemini-2.5-flash"
MAX_TOKENS: int = 8192

# Cache ayarları
CACHE_TTL_SECONDS: int = 600  # 10 dakika

# API Limitleri
MAX_SEARCH_RESULTS: int = 10
MIN_QUERY_LENGTH: int = 3
MAX_QUERY_LENGTH: int = 500
REQUEST_TIMEOUT_SECONDS: int = 30

# Uygulama Metadata
APP_TITLE: str = "Makale Arama"
APP_DESCRIPTION: str = "Gemini destekli akademik makale arama ve özetleme uygulaması"
APP_VERSION: str = "1.0.0"
