from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.scout import Business
from sqlalchemy import or_

class DeduplicationService:
    @staticmethod
    def deduplicate(new_businesses: List[Dict[str, Any]], db: Session) -> List[Dict[str, Any]]:
        """
        Check if businesses already exist in the database or within the new list itself.
        Returns only the unique, non-existing businesses.
        """
        unique_new = []
        seen_phones = set()
        seen_websites = set()
        
        for data in new_businesses:
            phone = data.get('phone')
            website = data.get('website')
            
            # Deduplicate against current batch
            if phone and phone in seen_phones:
                continue
            if website and website in seen_websites:
                continue
                
            # Deduplicate against DB
            filters = []
            if phone:
                filters.append(Business.phone == phone)
            if website:
                filters.append(Business.website == website)
                
            if filters:
                exists = db.query(Business).filter(Business.is_deleted == False, or_(*filters)).first()
                if exists:
                    # In a full implementation, we might MERGE data here.
                    # For now, we skip if it exists.
                    continue
            
            if phone:
                seen_phones.add(phone)
            if website:
                seen_websites.add(website)
                
            unique_new.append(data)
            
        return unique_new
