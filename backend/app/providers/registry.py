"""Provider registry — maps provider names to instances and manages availability."""
from typing import Dict, List, Optional
from loguru import logger

from app.providers.base.base_provider import BaseSearchProvider
from app.providers.searxng.provider import SearXNGProvider
from app.providers.brave.provider import BraveSearchProvider
from app.providers.duckduckgo.provider import DuckDuckGoProvider
from app.providers.google_places.provider import GooglePlacesProvider
from app.providers.website_discovery.provider import WebsiteDiscoveryProvider
from app.core.config import settings


_PROVIDER_MAP: Dict[str, BaseSearchProvider] = {
    "searxng": SearXNGProvider(),
    "brave": BraveSearchProvider(),
    "duckduckgo": DuckDuckGoProvider(),
    "google_places": GooglePlacesProvider(),
    "website_discovery": WebsiteDiscoveryProvider(),
}


def get_provider(name: str) -> Optional[BaseSearchProvider]:
    return _PROVIDER_MAP.get(name)


def get_all_providers() -> List[BaseSearchProvider]:
    """Return all registered providers sorted by priority."""
    providers = list(_PROVIDER_MAP.values())
    return sorted(providers, key=lambda p: p.priority)


def get_available_providers() -> List[BaseSearchProvider]:
    """Return only providers that have the necessary credentials."""
    available = []
    for p in get_all_providers():
        if p.name == "google_places" and not settings.GOOGLE_PLACES_API_KEY:
            logger.debug(f"[registry] Skipping {p.name} — no API key.")
            continue
        if p.name == "brave" and not settings.BRAVE_API_KEY:
            logger.debug(f"[registry] Skipping {p.name} — no API key.")
            continue
        available.append(p)
    return available


def get_providers_by_names(names: List[str]) -> List[BaseSearchProvider]:
    """Select specific providers by name, returning only those that exist."""
    result = []
    for name in names:
        provider = get_provider(name)
        if provider:
            result.append(provider)
        else:
            logger.warning(f"[registry] Unknown provider '{name}' requested.")
    return sorted(result, key=lambda p: p.priority)
