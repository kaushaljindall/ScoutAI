"""Google Places API provider — optional, gated behind GOOGLE_PLACES_API_KEY."""
import httpx
from typing import List, Optional
from loguru import logger
from aiolimiter import AsyncLimiter

from app.providers.base.base_provider import BaseSearchProvider, DiscoveredBusiness
from app.core.config import settings


class GooglePlacesProvider(BaseSearchProvider):
    """Searches Google Places API. Skipped if GOOGLE_PLACES_API_KEY is not set."""

    _limiter = AsyncLimiter(10, 1)
    TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    @property
    def name(self) -> str:
        return "google_places"

    @property
    def display_name(self) -> str:
        return "Google Places"

    @property
    def priority(self) -> int:
        return 2  # same priority as Brave

    def supports_location(self) -> bool:
        return True

    def supports_category(self) -> bool:
        return True

    def normalize(self, raw: dict) -> Optional[DiscoveredBusiness]:
        name = (raw.get("name") or "").strip()
        if not name:
            return None
        geometry = raw.get("geometry", {}).get("location", {})
        return DiscoveredBusiness(
            business_name=name,
            category=", ".join(raw.get("types", [])),
            address=raw.get("formatted_address"),
            city=self._extract_city(raw.get("address_components", [])),
            country=self._extract_country(raw.get("address_components", [])),
            latitude=geometry.get("lat"),
            longitude=geometry.get("lng"),
            google_rating=raw.get("rating"),
            review_count=raw.get("user_ratings_total"),
            phone=raw.get("formatted_phone_number"),
            website=raw.get("website"),
            provider=self.name,
            source_url=f"https://maps.google.com/?place_id={raw.get('place_id', '')}",
            provider_confidence=0.90,
            raw_data=raw,
        )

    def _extract_city(self, components: list) -> Optional[str]:
        for c in components:
            if "locality" in c.get("types", []):
                return c.get("long_name")
        return None

    def _extract_country(self, components: list) -> Optional[str]:
        for c in components:
            if "country" in c.get("types", []):
                return c.get("long_name")
        return None

    async def search(self, query: str, location: Optional[str] = None, max_results: int = 20) -> List[DiscoveredBusiness]:
        if not settings.GOOGLE_PLACES_API_KEY:
            logger.info("[google_places] GOOGLE_PLACES_API_KEY not set — skipping provider.")
            return []

        full_query = f"{query} in {location}" if location else query
        params = {
            "query": full_query,
            "key": settings.GOOGLE_PLACES_API_KEY,
        }

        async with self._limiter:
            async with httpx.AsyncClient(timeout=settings.SEARCH_PROVIDER_TIMEOUT) as client:
                resp = await client.get(self.TEXT_SEARCH_URL, params=params)
                resp.raise_for_status()
                data = resp.json()

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            logger.warning(f"[google_places] API error: {data.get('status')}")
            return []

        places = data.get("results", [])[:max_results]
        businesses = []
        for place in places:
            biz = self.normalize(place)
            if biz:
                businesses.append(biz)

        logger.info(f"[google_places] Returned {len(businesses)} results for '{full_query}'")
        return businesses

    async def health_check(self) -> bool:
        if not settings.GOOGLE_PLACES_API_KEY:
            return False
        try:
            params = {"query": "test", "key": settings.GOOGLE_PLACES_API_KEY}
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(self.TEXT_SEARCH_URL, params=params)
                data = resp.json()
                return data.get("status") in ("OK", "ZERO_RESULTS", "REQUEST_DENIED")
        except Exception:
            return False
