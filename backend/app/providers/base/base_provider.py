from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone


class DiscoveredBusiness(BaseModel):
    """Normalized business record returned by any provider."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    business_name: str
    category: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    google_rating: Optional[float] = None
    review_count: Optional[int] = None
    provider: str
    source_url: Optional[str] = None
    provider_confidence: float = 0.5  # 0.0 - 1.0
    raw_data: Optional[dict] = None
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BaseSearchProvider(ABC):
    """Abstract base class for all search providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique provider identifier slug."""
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable provider name."""
        ...

    @property
    @abstractmethod
    def priority(self) -> int:
        """Execution priority — lower runs first."""
        ...

    @abstractmethod
    def supports_location(self) -> bool:
        """Whether this provider supports location filtering."""
        ...

    @abstractmethod
    def supports_category(self) -> bool:
        """Whether this provider supports category filtering."""
        ...

    @abstractmethod
    async def search(self, query: str, location: Optional[str] = None, max_results: int = 20) -> List[DiscoveredBusiness]:
        """Execute search and return raw results."""
        ...

    @abstractmethod
    def normalize(self, raw: dict) -> Optional[DiscoveredBusiness]:
        """Normalize a raw provider response dict into a DiscoveredBusiness."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if provider is reachable and operational."""
        ...

    async def safe_search(self, query: str, location: Optional[str] = None, max_results: int = 20) -> List[DiscoveredBusiness]:
        """Wrapper around search() that never throws — returns empty list on failure."""
        try:
            return await self.search(query, location, max_results)
        except Exception as e:
            from loguru import logger
            logger.warning(f"[{self.name}] safe_search caught error: {e}")
            return []
