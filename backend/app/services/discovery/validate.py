import re
from typing import Dict, Any

class ValidationService:
    @staticmethod
    def validate_email(email: str) -> bool:
        if not email:
            return False
        # Basic regex for email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_website_reachable(website: str) -> str:
        """
        Mock validation for website reachability.
        In production, this would make an actual HTTP request (e.g., using httpx)
        and check for 200 OK, SSL validity, redirects, etc.
        """
        if not website:
            return "unknown"
        # Since this is synchronous and we don't want to block, we mock it.
        # Could return "reachable", "unreachable", "invalid_ssl"
        return "reachable"

    @staticmethod
    def validate_business_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and enrich with validation status.
        """
        validated = data.copy()
        
        if 'email' in validated and validated['email']:
            if not ValidationService.validate_email(validated['email']):
                validated['email'] = None # Invalid email removed
                
        if 'website' in validated and validated['website']:
            validated['website_status'] = ValidationService.validate_website_reachable(validated['website'])
            
        return validated
