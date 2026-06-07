"""
main.py — FastAPI uygulamasının ana dosyası
"""

import logging
import os
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from makale_arama_projesi import gemini_client
from makale_arama_projesi.cache import search_cache, summary_cache
from makale_arama_projesi.config import APP_DESCRIPTION, APP_TITLE, APP_VERSION
from makale_arama_projesi.models import (
    ErrorResponse,
    SearchRequest,
    SearchResponse,
    SummarizeRequest,
    SummarizeResponse,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# FastAPI uygulaması
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# HTML şablon dizini
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


# ---------------------------------------------------------------------------
# Yaşam döngüsü olayları
# ---------------------------------------------------------------------------


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Uygulama başlatılıyor — %s v%s", APP_TITLE, APP_VERSION)
    # Config doğrulaması config.py import sırasında gerçekleşir.
    logger.info("Gemini istemcisi hazır, model: gemini-2.0-flash")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("Uygulama durduruluyor — cache temizleniyor")
    search_cache.clear()
    summary_cache.clear()


# ---------------------------------------------------------------------------
# Hata yöneticileri
# ---------------------------------------------------------------------------


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=f"HTTP_{exc.status_code}",
            message=exc.detail,
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    field_info = ", ".join(
        f"{'.'.join(str(loc) for loc in e['loc'])}: {e['msg']}" for e in errors
    )
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="İstek doğrulama hatası",
            detail=field_info,
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Beklenmeyen hata: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="Sunucu iç hatası. Lütfen daha sonra tekrar deneyin.",
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Endpoint'ler
# ---------------------------------------------------------------------------


@app.get("/", summary="Ana Sayfa")
async def index() -> FileResponse:
    """Ana sayfa HTML'ini döndürür."""
    html_path = os.path.join(TEMPLATES_DIR, "index.html")
    return FileResponse(html_path, media_type="text/html")


@app.get("/api/health", summary="Sağlık Kontrolü")
async def health_check() -> dict:
    """Sistem sağlık kontrolü endpoint'i."""
    return {
        "status": "ok",
        "search_cache_size": len(search_cache),
        "summary_cache_size": len(summary_cache),
    }


@app.post("/api/search", response_model=SearchResponse, summary="Makale Arama")
async def search_articles(body: SearchRequest) -> SearchResponse:
    """
    Gemini API kullanarak akademik makale arar.
    Sonuçlar 10 dakika cache'lenir.
    """
    cache_key = search_cache.make_key(f"{body.query}::{body.language}")
    cached = search_cache.get(cache_key)

    if cached is not None:
        logger.info("Cache hit — query: %s", body.query)
        return cached

    logger.info("Cache miss — Gemini'ye istek gönderiliyor: %s", body.query)
    start_ms = time.time() * 1000

    results = await gemini_client.search_articles(body.query, body.language)

    duration_ms = time.time() * 1000 - start_ms

    response = SearchResponse(
        query=body.query,
        results=results,
        total_count=len(results),
        search_duration_ms=round(duration_ms, 2),
    )

    search_cache.set(cache_key, response)
    return response


@app.post("/api/summarize", response_model=SummarizeResponse, summary="Makale Özetleme")
async def summarize_article(body: SummarizeRequest) -> SummarizeResponse:
    """
    Gemini API kullanarak makaleyi özetler.
    Sonuçlar DOI veya başlık hash'iyle cache'lenir.
    """
    raw_key = body.doi if body.doi else body.title
    cache_key = summary_cache.make_key(raw_key)
    cached = summary_cache.get(cache_key)

    if cached is not None:
        logger.info("Summary cache hit — key: %s", raw_key[:50])
        return cached

    logger.info("Özetleme isteği — title: %s", body.title[:80])
    result = await gemini_client.summarize_article(body.title, body.abstract)
    summary_cache.set(cache_key, result)
    return result
