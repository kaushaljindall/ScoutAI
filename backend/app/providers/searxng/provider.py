"""SearXNG provider — JSON API with HTML scraping fallback."""
import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from loguru import logger
from aiolimiter import AsyncLimiter

from app.providers.base.base_provider import BaseSearchProvider, DiscoveredBusiness
from app.core.config import settings

# Public SearXNG instances — tried in order
_FALLBACK_INSTANCES = [
    "https://search.inetol.net",
    "https://searx.tiekoetter.com",
    "https://paulgo.io",
    "https://opnxng.com",
    "https://searxng.world",
]

_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
}


class SearXNGProvider(BaseSearchProvider):
    """Searches SearXNG via HTML scraping (public instances have JSON API disabled)."""

    _limiter = AsyncLimiter(2, 1)  # 2 requests/second — be polite to public instances

    @property
    def name(self) -> str:
        return "searxng"

    @property
    def display_name(self) -> str:
        return "SearXNG"

    @property
    def priority(self) -> int:
        return 1

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
            address=raw.get("content", "")[:200] if raw.get("content") else None,
            provider=self.name,
            source_url=raw.get("url"),
            provider_confidence=0.60,
            raw_data=raw,
        )

    def _parse_html(self, html: str, max_results: int) -> List[dict]:
        """Parse SearXNG HTML result page into raw dicts."""
        soup = BeautifulSoup(html, "lxml")
        raw_results = []

        # SearXNG uses <article class="result"> or <div class="result">
        for result in soup.select("article.result, div.result")[:max_results]:
            title_tag = result.select_one("h3 a, h4 a")
            snippet_tag = result.select_one("p.content, .result-content, .content")
            if title_tag:
                raw_results.append({
                    "title": title_tag.get_text(strip=True),
                    "url": title_tag.get("href"),
                    "content": snippet_tag.get_text(strip=True) if snippet_tag else None,
                })

        return raw_results

    def _get_instances(self) -> List[str]:
        """Return configured URL first, then public fallbacks (deduped)."""
        configured = settings.SEARXNG_BASE_URL.rstrip("/")
        seen = {configured}
        instances = [configured]
        for fb in _FALLBACK_INSTANCES:
            if fb not in seen:
                seen.add(fb)
                instances.append(fb)
        return instances

    async def _try_instance(self, base_url: str, query: str, max_results: int) -> Optional[List[dict]]:
        """Try one instance — pre-fetches homepage to satisfy cookie gates, then scrapes search HTML."""
        params = {"q": query, "categories": "general", "language": "en"}
        try:
            async with httpx.AsyncClient(
                timeout=settings.SEARCH_PROVIDER_TIMEOUT,
                headers=_BROWSER_HEADERS,
                follow_redirects=True,
            ) as client:
                # Pre-fetch homepage to receive session cookies (required by most public instances)
                await client.get(base_url)

                resp = await client.get(f"{base_url}/search", params=params)

            if resp.status_code == 403:
                logger.debug(f"[searxng] {base_url} returned 403 — skipping")
                return None

            resp.raise_for_status()

            # If we were silently redirected back to the homepage, the page will be short / have no results
            content_type = resp.headers.get("content-type", "")
            if "json" in content_type:
                data = resp.json()
                results = data.get("results", [])[:max_results]
                if results:
                    return results

            # HTML scraping path
            raw = self._parse_html(resp.text, max_results)
            if not raw:
                logger.debug(f"[searxng] {base_url} returned HTML but no results could be parsed")
                return None

            return raw

        except Exception as e:
            logger.debug(f"[searxng] {base_url} failed: {e}")
            return None

    async def search(self, query: str, location: Optional[str] = None, max_results: int = 20) -> List[DiscoveredBusiness]:
        full_query = f"{query} {location}" if location else query

        async with self._limiter:
            raw_results = None
            for instance in self._get_instances():
                raw_results = await self._try_instance(instance, full_query, max_results)
                if raw_results is not None:
                    logger.info(f"[searxng] Using instance: {instance} ({len(raw_results)} raw results)")
                    break

        if not raw_results:
            logger.warning("[searxng] All instances failed or returned no parseable results.")
            return []

        businesses = []
        for item in raw_results:
            biz = self.normalize(item)
            if biz:
                businesses.append(biz)

        logger.info(f"[searxng] Returned {len(businesses)} results for '{full_query}'")
        return businesses

    async def health_check(self) -> bool:
        for instance in self._get_instances():
            try:
                async with httpx.AsyncClient(timeout=5, headers=_BROWSER_HEADERS, follow_redirects=True) as client:
                    resp = await client.get(f"{instance}/search", params={"q": "test"})
                    if resp.status_code == 200 and len(resp.text) > 500:
                        return True
            except Exception:
                continue
        return False
