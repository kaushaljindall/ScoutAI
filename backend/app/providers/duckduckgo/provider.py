"""DuckDuckGo provider — uses public HTML scraping (no API key needed)."""
import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from loguru import logger
from aiolimiter import AsyncLimiter
from fake_useragent import UserAgent

from app.providers.base.base_provider import BaseSearchProvider, DiscoveredBusiness
from app.core.config import settings

_ua = UserAgent()


class DuckDuckGoProvider(BaseSearchProvider):
    """Scrapes DuckDuckGo HTML results for business listings."""

    _limiter = AsyncLimiter(2, 1)  # 2 req/second

    @property
    def name(self) -> str:
        return "duckduckgo"

    @property
    def display_name(self) -> str:
        return "DuckDuckGo"

    @property
    def priority(self) -> int:
        return 3

    def supports_location(self) -> bool:
        return True

    def supports_category(self) -> bool:
        return True

    def normalize(self, raw: dict) -> Optional[DiscoveredBusiness]:
        title = (raw.get("title") or "").strip()
        if not title:
            return None
        return DiscoveredBusiness(
            business_name=title,
            website=raw.get("url"),
            address=raw.get("snippet", "")[:200] if raw.get("snippet") else None,
            provider=self.name,
            source_url=raw.get("url"),
            provider_confidence=0.50,
            raw_data=raw,
        )

    async def search(self, query: str, location: Optional[str] = None, max_results: int = 20) -> List[DiscoveredBusiness]:
        full_query = f"{query} {location}" if location else query
        headers = {
            "User-Agent": _ua.random,
            "Accept-Language": "en-US,en;q=0.9",
        }
        params = {"q": full_query, "ia": "web"}

        async with self._limiter:
            async with httpx.AsyncClient(
                timeout=settings.SEARCH_PROVIDER_TIMEOUT,
                follow_redirects=True,
                headers=headers,
            ) as client:
                resp = await client.get("https://html.duckduckgo.com/html/", params=params)
                resp.raise_for_status()
                html = resp.text

        soup = BeautifulSoup(html, "lxml")
        raw_results = []
        for result in soup.select(".result__body")[:max_results]:
            title_tag = result.select_one(".result__title a")
            snippet_tag = result.select_one(".result__snippet")
            if title_tag:
                raw_results.append({
                    "title": title_tag.get_text(strip=True),
                    "url": title_tag.get("href"),
                    "snippet": snippet_tag.get_text(strip=True) if snippet_tag else None,
                })

        businesses = []
        for item in raw_results:
            biz = self.normalize(item)
            if biz:
                businesses.append(biz)

        logger.info(f"[duckduckgo] Returned {len(businesses)} results for '{full_query}'")
        return businesses

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
                resp = await client.get("https://html.duckduckgo.com/html/", params={"q": "test"})
                return resp.status_code == 200
        except Exception:
            return False
