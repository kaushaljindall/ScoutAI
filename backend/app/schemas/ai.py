from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID

class AIAnalysisResult(BaseModel):
    summary_short: str
    summary_medium: str
    summary_long: str
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    opportunity_score: int
    confidence_score: float
    ai_tags: List[str]
    estimated_budget: str
    recommended_services: List[str]
    
class BusinessAnalysisResponse(AIAnalysisResult):
    id: UUID
    business_id: UUID

    model_config = ConfigDict(from_attributes=True)
