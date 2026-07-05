from abc import ABC, abstractmethod
from typing import Dict, Any, Type
import json
from google import genai
from pydantic import BaseModel

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> BaseModel:
        """
        Generate structured output based on a Pydantic schema
        """
        pass

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str = 'gemini-2.5-flash'):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate_structured(self, prompt: str, schema: Type[BaseModel]) -> BaseModel:
        # In the new genai SDK, we use response_schema to force structure
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                },
            )
            data = json.loads(response.text)
            return schema(**data)
        except Exception as e:
            # Re-raise for retry logic in higher levels
            raise RuntimeError(f"Gemini AI generation failed: {str(e)}")
