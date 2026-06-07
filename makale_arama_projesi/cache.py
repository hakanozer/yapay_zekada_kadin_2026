"""
cache.py — In-memory cache katmanı (TTL destekli)
"""

import hashlib
import time
from typing import Any, Optional

from makale_arama_projesi.config import CACHE_TTL_SECONDS


class CacheEntry:
    """Tek bir cache girdisini TTL ile birlikte tutar."""

    def __init__(self, value: Any, ttl: int = CACHE_TTL_SECONDS) -> None:
        self.value = value
        self.expires_at: float = time.time() + ttl

    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class InMemoryCache:
    """
    SHA-256 tabanlı in-memory cache.
    Arama sonuçları ve özetler ayrı namespace'lerde saklanır.
    """

    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}

    @staticmethod
    def make_key(raw: str) -> str:
        """Ham string'den SHA-256 hash üretir."""
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Anahtara karşılık gelen değeri döndürür.
        Süre dolmuşsa None döner ve girdiyi temizler.
        """
        entry = self._store.get(key)
        if entry is None:
            return None
        if entry.is_expired():
            del self._store[key]
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl: int = CACHE_TTL_SECONDS) -> None:
        """Anahtara karşılık değeri TTL süresiyle cache'e yazar."""
        self._store[key] = CacheEntry(value, ttl)

    def invalidate(self, key: str) -> None:
        """Belirtilen anahtarı cache'den siler."""
        self._store.pop(key, None)

    def clear(self) -> None:
        """Tüm cache'i temizler."""
        self._store.clear()

    def __len__(self) -> int:
        """Cache'deki aktif (süresi dolmamış) girdi sayısını döndürür."""
        now = time.time()
        return sum(1 for e in self._store.values() if not e.is_expired())


# Uygulama genelinde kullanılacak cache örnekleri
search_cache = InMemoryCache()
summary_cache = InMemoryCache()
