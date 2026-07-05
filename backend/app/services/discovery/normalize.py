import re
from typing import Dict, Any

class NormalizationService:
    @staticmethod
    def normalize_phone(phone: str) -> str:
        if not phone:
            return None
        # Keep only digits and '+'
        normalized = re.sub(r'[^\d+]', '', phone)
        return normalized

    @staticmethod
    def normalize_website(website: str) -> str:
        if not website:
            return None
        website = website.lower().strip()
        if not website.startswith('http://') and not website.startswith('https://'):
            website = f'https://{website}'
        return website

    @staticmethod
    def normalize_business_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw business data from providers.
        """
        normalized = raw_data.copy()
        
        if 'phone' in normalized:
            normalized['phone'] = NormalizationService.normalize_phone(normalized['phone'])
            
        if 'website' in normalized:
            normalized['website'] = NormalizationService.normalize_website(normalized['website'])
            
        if 'email' in normalized and normalized['email']:
            normalized['email'] = normalized['email'].lower().strip()
            
        if 'business_name' in normalized and normalized['business_name']:
            normalized['business_name'] = normalized['business_name'].strip()
            
        return normalized
