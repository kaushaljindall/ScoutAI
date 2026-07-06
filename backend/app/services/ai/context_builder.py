import json
from app.models.validation import ValidatedBusiness

class ContextBuilder:
    @staticmethod
    def build_business_context(business: ValidatedBusiness) -> str:
        """
        Builds a clean, text-based context representation of a validated business
        to pass into the LLM prompt. Never passes raw DB objects directly.
        """
        context = []
        context.append(f"Business Name: {business.business_name}")
        
        if business.description:
            context.append(f"Description: {business.description}")
            
        if business.services:
            context.append(f"Services: {', '.join(business.services)}")
            
        location = ", ".join(filter(None, [business.city, business.state, business.country]))
        if location:
            context.append(f"Location: {location}")
            
        if business.social_links:
            context.append("Social Links:")
            for platform, url in business.social_links.items():
                context.append(f"- {platform}: {url}")
                
        if business.website:
            context.append("\n--- Website Intelligence ---")
            context.append(f"URL: {business.website.url}")
            context.append(f"Is Reachable: {business.website.is_reachable}")
            context.append(f"HTTPS Enabled: {business.website.https_enabled}")
            if business.website.tech_stack:
                context.append(f"Tech Stack: {', '.join(business.website.tech_stack)}")
            context.append(f"Has Booking System: {business.website.has_booking_system}")
            context.append(f"Has Contact Form: {business.website.has_contact_form}")

        context.append("\n--- Contact Information ---")
        for contact in business.contacts:
            valid_str = "Valid" if contact.is_valid else "Unverified"
            context.append(f"- {contact.contact_type.value}: {contact.value} ({valid_str})")
            
        return "\n".join(context)
