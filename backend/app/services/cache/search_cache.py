"""In-memory TTL cache for search results."""
import hashlib
import json
from typing import Any, Optional
from cachetools import TTLCache
from loguru import logger

from app.core.config import settings

# Max 500 cached searches, TTL from settings (default 15 min)
_cache: TTLCache = TTLCache(maxsize=500, ttl=settings.SEARCH_CACHE_TTL_SECONDS)


def _make_key(query: str, location: Optional[str], providers: list) -> str:
    raw = json.dumps({"q": query.lower().strip(), "loc": (location or "").lower().strip(), "p": sorted(providers)}, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cached(query: str, location: Optional[str], providers: list) -> Optional[Any]:
    key = _make_key(query, location, providers)
    result = _cache.get(key)
    if result is not None:
        logger.info(f"[cache] HIT for key={key[:12]}...")
    return result


def set_cached(query: str, location: Optional[str], providers: list, value: Any) -> None:
    key = _make_key(query, location, providers)
    _cache[key] = value
    logger.info(f"[cache] SET for key={key[:12]}... ({len(_cache)}/{_cache.maxsize} entries)")


def invalidate(query: str, location: Optional[str], providers: list) -> None:
    key = _make_key(query, location, providers)
    _cache.pop(key, None)


def clear_all() -> None:
    _cache.clear()
