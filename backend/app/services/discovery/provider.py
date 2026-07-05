from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProvider(ABC):
    @abstractmethod
    def search(self, query: str, location: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for businesses and return a list of raw dictionaries
        """
        pass

class MockProvider(BaseProvider):
    """
    A mock provider for discovery when external APIs are not connected.
    """
    def search(self, query: str, location: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        # Mocking discovery logic
        results = []
        for i in range(limit):
            results.append({
                "business_name": f"Discovered {query} {i+1}",
                "category": "Discovered Category",
                "phone": f"+1234567890{i}",
                "email": f"contact{i}@discovered.com",
                "website": f"www.discovered{i}.com",
                "city": location or "Unknown City",
                "source": "MockProvider",
                "google_rating": 4.5,
                "review_count": 100 + i,
                "confidence_score": 0.95
            })
        return results
