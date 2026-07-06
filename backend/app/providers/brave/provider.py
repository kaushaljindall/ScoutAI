"""Brave Search provider."""
import httpx
from typing import List, Optional
from loguru import logger
from aiolimiter import AsyncLimiter

from app.providers.base.base_provider import BaseSearchProvider, DiscoveredBusiness
from app.core.config import settings


class BraveSearchProvider(BaseSearchProvider):
    """Uses Brave Search API to find businesses."""

    _limiter = AsyncLimiter(1, 1)  # 1 req/second (free tier)
    BASE_URL = "https://api.search.brave.com/res/v1/web/search"

    @property
    def name(self) -> str:
        return "brave"

    @property
    def display_name(self) -> str:
        return "Brave Search"

    @property
    def priority(self) -> int:
        return 2

    def supports_location(self) -> bool:
        return True

    def supports_category(self) -> bool:
        return True

    def normalize(self, raw: dict) -> Optional[DiscoveredBusiness]:
        title = (raw.get("title") or "").strip()
        if not title:
            return None
        desc = raw.get("description") or ""
        return DiscoveredBusiness(
            business_name=title,
            website=raw.get("url"),
            address=desc[:200] if desc else None,
            provider=self.name,
            source_url=raw.get("url"),
            provider_confidence=0.65,
            raw_data=raw,
        )

    async def search(self, query: str, location: Optional[str] = None, max_results: int = 20) -> List[DiscoveredBusiness]:
        if not settings.BRAVE_API_KEY:
            logger.warning("[brave] No API key configured, skipping.")
            return []

        full_query = f"{query} {location}" if location else query
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": settings.BRAVE_API_KEY,
        }
        params = {"q": full_query, "count": min(max_results, 20)}

        async with self._limiter:
            async with httpx.AsyncClient(timeout=settings.SEARCH_PROVIDER_TIMEOUT) as client:
                resp = await client.get(self.BASE_URL, headers=headers, params=params)
                resp.raise_for_status()
                data = resp.json()

        web_results = data.get("web", {}).get("results", [])[:max_results]
        businesses = []
        for item in web_results:
            biz = self.normalize(item)
            if biz:
                businesses.append(biz)
        logger.info(f"[brave] Returned {len(businesses)} results for '{full_query}'")
        return businesses

    async def health_check(self) -> bool:
        if not settings.BRAVE_API_KEY:
            return False
        try:
            headers = {"Accept": "application/json", "X-Subscription-Token": settings.BRAVE_API_KEY}
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(self.BASE_URL, headers=headers, params={"q": "test", "count": 1})
                return resp.status_code == 200
        except Exception:
            return False
