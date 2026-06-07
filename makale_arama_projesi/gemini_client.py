"""
gemini_client.py — Gemini API istemcisi ve iş mantığı
"""

import json
import logging
from typing import Any

from fastapi import HTTPException
from google import genai
from google.genai import types

from makale_arama_projesi.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_SEARCH_RESULTS,
    REQUEST_TIMEOUT_SECONDS,
)
from makale_arama_projesi.models import ArticleResult, SummarizeResponse

logger = logging.getLogger(__name__)

# Gemini istemcisini başlat
client = genai.Client(api_key=GEMINI_API_KEY)


async def search_articles(query: str, language: str = "tr") -> list[ArticleResult]:
    """
    Gemini API ile akademik makale arama.
    Grounding (Google Search) özelliği etkindir.
    """

    lang_instruction = (
        "Yanıtları Türkçe olarak ver." if language == "tr" else "Respond in English."
    )

    system_prompt = f"""Sen bir akademik makale arama asistanısın. {lang_instruction}

Kurallar:
- YALNIZCA hakemli (peer-reviewed) akademik makaleler döndür
- Güvenilir kaynaklar: PubMed, arXiv, IEEE Xplore, Springer, Elsevier, Nature, Science, JSTOR
- Her sonuç için şu alanları mutlaka doldur: title, authors, year, source, abstract, relevance_score
- doi veya url alanlarından en az birini doldur
- Sonuçları alaka düzeyine göre sırala (en alakalı önce)
- Maksimum {MAX_SEARCH_RESULTS} sonuç döndür
- abstract alanını 200-300 kelime arasında tut
- relevance_score 0.0 ile 1.0 arasında olmalı

YANITI SADECE GEÇERLİ JSON OLARAK DÖNDÜR, başka hiçbir metin ekleme:
{{
  "results": [
    {{
      "title": "makale başlığı",
      "authors": "Yazar1, Yazar2",
      "year": "2024",
      "source": "Dergi/Kaynak adı",
      "abstract": "Makale özeti...",
      "doi": "10.xxxx/xxxxx",
      "url": "https://...",
      "relevance_score": 0.95
    }}
  ]
}}"""

    user_prompt = f"Şu konuda akademik makaleler ara: {query}"

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=0.2,
                max_output_tokens=8192,
            ),
        )

        raw_text = response.text.strip()

        # JSON bloğunu temizle
        raw_text = _extract_json(raw_text)

        data: dict[str, Any] = json.loads(raw_text)
        results_data = data.get("results", [])

        articles: list[ArticleResult] = []
        for item in results_data:
            try:
                article = ArticleResult(**item)
                articles.append(article)
            except Exception as e:
                logger.warning("Makale parse hatası, atlanıyor: %s — %s", item.get("title"), e)

        return articles

    except json.JSONDecodeError as e:
        logger.error("Gemini JSON parse hatası: %s", e)
        raise HTTPException(
            status_code=502,
            detail="Gemini API'den geçersiz JSON yanıtı alındı. Lütfen tekrar deneyin.",
        )
    except Exception as e:
        logger.error("Makale arama hatası: %s", e)
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API hatası: {str(e)}",
        )


async def summarize_article(title: str, abstract: str) -> SummarizeResponse:
    """
    Gemini API ile makale özetleme.
    """

    system_prompt = """Sen bir akademik makale özetleme asistanısın. Türkçe yanıt ver.

Görevin:
1. Makalenin ana argümanını 2-3 cümleyle özetle
2. Kullanılan metodoloji nedir?
3. Temel bulgular ve sonuçlar nelerdir?
4. 3-5 madde halinde anahtar çıkarımlar listele
5. Akademik olmayan okuyucu için sade dil kullan
6. Gereksiz tekrar ve jargon içerme

YANITI SADECE GEÇERLİ JSON OLARAK DÖNDÜR:
{
  "summary": "Ana argümanı açıklayan 2-3 cümle...",
  "methodology": "Kullanılan araştırma yöntemi...",
  "findings": "Temel bulgular ve sonuçlar...",
  "key_points": [
    "Anahtar çıkarım 1",
    "Anahtar çıkarım 2",
    "Anahtar çıkarım 3"
  ]
}"""

    user_prompt = f"""Başlık: {title}

Özet: {abstract}"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3,
                max_output_tokens=2048,
            ),
        )

        raw_text = response.text.strip()
        raw_text = _extract_json(raw_text)

        data: dict[str, Any] = json.loads(raw_text)

        return SummarizeResponse(
            summary=data.get("summary", ""),
            key_points=data.get("key_points", []),
            methodology=data.get("methodology", ""),
            findings=data.get("findings", ""),
        )

    except json.JSONDecodeError as e:
        logger.error("Gemini JSON parse hatası (özetleme): %s", e)
        raise HTTPException(
            status_code=502,
            detail="Gemini API'den geçersiz JSON yanıtı alındı. Lütfen tekrar deneyin.",
        )
    except Exception as e:
        logger.error("Özetleme hatası: %s", e)
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API hatası: {str(e)}",
        )


def _extract_json(text: str) -> str:
    """
    Metin içinden JSON bloğunu çıkarır.
    Markdown kod bloğu (```json ... ```) varsa temizler.
    """
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.rindex("```")
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        end = text.rindex("```")
        return text[start:end].strip()
    # JSON'ın başladığı ilk { ya da [ karakterini bul
    for i, ch in enumerate(text):
        if ch in ("{", "["):
            return text[i:]
    return text
