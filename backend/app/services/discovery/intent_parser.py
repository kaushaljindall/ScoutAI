import json
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.services.ai.provider import GeminiProvider
from app.core.config import settings

class SearchIntent(BaseModel):
    category: str
    city: Optional[str] = None
    country: Optional[str] = None
    limit: int = 10
    special_requirements: list[str] = []

class IntentParser:
    def __init__(self):
        self.provider = GeminiProvider(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None

    async def parse(self, query: str) -> SearchIntent:
        if not self.provider:
            # Fallback if no AI key
            return SearchIntent(category=query, limit=5)

        prompt = f"""
        You are an expert AI intent parser for a B2B lead generation tool called ScoutAI.
        The user has entered the following natural language query: "{query}"
        
        Extract the search parameters and return a valid JSON object matching this schema exactly:
        {{
            "category": "The specific business category (e.g., 'Dental Clinic', 'Interior Designer')",
            "city": "The city mentioned, if any",
            "country": "The country mentioned, if any",
            "limit": number of results requested (default to 10 if not specified),
            "special_requirements": ["list of specific things they are looking for, e.g., 'outdated website', 'no whatsapp button'"]
        }}
        
        Return ONLY valid JSON, without any markdown formatting or extra text.
        """
        
        try:
            def generate():
                return self.provider.generate_structured(prompt, SearchIntent)
                
            response = await asyncio.to_thread(generate)
            return response
        except Exception as e:
            print(f"⚠️ Intent parsing failed: {e}. Falling back to keyword search.")
            return SearchIntent(category=query, limit=5)
