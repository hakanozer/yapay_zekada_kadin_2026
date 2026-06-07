"""
models.py — Pydantic request/response şemaları
"""

from typing import Optional
from pydantic import BaseModel, field_validator, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500, description="Arama sorgusu")
    language: str = Field(default="tr", description="Yanıt dili (tr/en)")

    @field_validator("query")
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Arama sorgusu boş olamaz")
        return v.strip()

    @field_validator("language")
    @classmethod
    def language_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Dil alanı boş olamaz")
        return v.strip().lower()


class ArticleResult(BaseModel):
    title: str = Field(..., description="Makale başlığı")
    authors: str = Field(..., description="Yazarlar")
    year: Optional[str] = Field(default=None, description="Yayın yılı")
    source: str = Field(..., description="Kaynak / Dergi adı")
    abstract: str = Field(..., description="Özet")
    doi: Optional[str] = Field(default=None, description="DOI numarası")
    url: Optional[str] = Field(default=None, description="Makale URL'i")
    relevance_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Alaka düzeyi skoru (0-1)"
    )

    @field_validator("title", "authors", "source", "abstract")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Alan boş olamaz")
        return v.strip()


class SearchResponse(BaseModel):
    query: str = Field(..., description="Yapılan arama sorgusu")
    results: list[ArticleResult] = Field(default_factory=list, description="Makale sonuçları")
    total_count: int = Field(..., description="Toplam sonuç sayısı")
    search_duration_ms: float = Field(..., description="Arama süresi (ms)")


class SummarizeRequest(BaseModel):
    title: str = Field(..., description="Makale başlığı")
    abstract: str = Field(..., description="Makale özeti")
    doi: Optional[str] = Field(default=None, description="DOI numarası")

    @field_validator("title", "abstract")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Alan boş olamaz")
        return v.strip()


class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="Genel özet (2-3 cümle)")
    key_points: list[str] = Field(default_factory=list, description="Anahtar çıkarımlar")
    methodology: str = Field(..., description="Kullanılan metodoloji")
    findings: str = Field(..., description="Temel bulgular ve sonuçlar")


class ErrorResponse(BaseModel):
    error_code: str = Field(..., description="Hata kodu")
    message: str = Field(..., description="Hata mesajı")
    detail: Optional[str] = Field(default=None, description="Hata detayı")
