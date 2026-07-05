import time
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.services.discovery.provider import MockProvider
from app.services.discovery.normalize import NormalizationService
from app.services.discovery.validate import ValidationService
from app.services.discovery.deduplicate import DeduplicationService
from app.services.discovery.storage import BusinessStorageService
from app.models.scout import SearchHistory

class DiscoveryPipeline:
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
        # We can dynamically inject providers here later
        self.provider = MockProvider()
        
    def run(self, query: str, location: str = None, max_results: int = 10, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Discover
        raw_businesses = self.provider.search(query, location=location, limit=max_results)
        
        # 2. Normalize & 3. Validate
        processed_businesses = []
        for raw in raw_businesses:
            normalized = NormalizationService.normalize_business_data(raw)
            validated = ValidationService.validate_business_data(normalized)
            processed_businesses.append(validated)
            
        # 4. Deduplicate
        unique_businesses = DeduplicationService.deduplicate(processed_businesses, self.db)
        
        # 5. Save to Database
        if unique_businesses:
            BusinessStorageService.save_businesses(unique_businesses, self.db)
            
        execution_time = time.time() - start_time
        
        # 6. Save Search History
        history = SearchHistory(
            user_id=self.user_id,
            search_query=query,
            filters=filters or {},
            results_count=len(unique_businesses),
            execution_time=execution_time
        )
        self.db.add(history)
        self.db.commit()
        
        return {
            "status": "success",
            "businesses_discovered": len(unique_businesses),
            "execution_time": execution_time
        }
