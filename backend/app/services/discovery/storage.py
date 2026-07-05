from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.scout import Business
from datetime import datetime

class BusinessStorageService:
    @staticmethod
    def save_businesses(businesses_data: List[Dict[str, Any]], db: Session) -> List[Business]:
        saved_businesses = []
        for data in businesses_data:
            business = Business(
                business_name=data.get('business_name'),
                category=data.get('category'),
                phone=data.get('phone'),
                email=data.get('email'),
                website=data.get('website'),
                city=data.get('city'),
                state=data.get('state'),
                country=data.get('country'),
                google_rating=data.get('google_rating'),
                review_count=data.get('review_count', 0),
                source=data.get('source'),
                confidence_score=data.get('confidence_score'),
                website_status=data.get('website_status'),
                last_checked=datetime.utcnow()
            )
            db.add(business)
            saved_businesses.append(business)
            
        db.commit()
        for b in saved_businesses:
            db.refresh(b)
            
        return saved_businesses
