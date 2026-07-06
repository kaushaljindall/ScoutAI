import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from beanie import Link, Document
from enum import Enum

from app.models.base import BaseDocument
from app.models.validation import ValidatedBusiness

class OpportunityReason(BaseModel):
    reason: str
    impact: str # "positive", "negative", "neutral"

class OpportunityScore(BaseModel):
    score: int = Field(ge=0, le=100)
    reasons: List[OpportunityReason] = Field(default_factory=list)
    explanation: str

class Recommendation(BaseModel):
    service_name: str
    reasoning: str
    estimated_impact: str # e.g. "High", "Medium", "Low"
    estimated_effort: str # e.g. "High", "Medium", "Low"

class AIExecution(BaseModel):
    prompt_version: str
    execution_time: float
    token_usage: int
    llm_provider: str
    model_name: str
    retry_count: int = 0
    validation_errors: int = 0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BusinessIntelligence(BaseDocument):
    """
    AI Business Intelligence report for a Validated Business.
    """
    business_id: uuid.UUID = Field(index=True)
    
    # Core Analysis
    executive_summary: str
    detailed_summary: str
    business_category: str
    industry: str
    business_size: str
    target_audience: str
    
    # Maturity & Quality
    digital_maturity: str
    website_quality: str
    brand_quality: str
    seo_quality: str
    technology_maturity: str
    online_presence: str
    estimated_marketing_maturity: str
    
    # Financials & Opportunity
    estimated_budget_range: str
    growth_potential: str
    decision_maker_guess: str
    estimated_project_value: str
    sales_difficulty: str
    
    # SWOT
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    
    # Actions
    next_best_action: str
    
    # Embedded Sub-Documents
    opportunity_score: OpportunityScore
    recommendations: List[Recommendation] = Field(default_factory=list)
    ai_tags: List[str] = Field(default_factory=list)
    
    # Metadata
    ai_confidence: float = Field(ge=0.0, le=1.0)
    executions: List[AIExecution] = Field(default_factory=list)

    class Settings:
        name = "business_intelligence"
        indexes = [
            "business_id",
        ]

class PromptVersion(BaseDocument):
    """
    Tracks versions of AI prompts used for analysis.
    """
    name: str = Field(index=True)
    version: str = Field(index=True)
    template: str
    description: Optional[str] = None
    is_active: bool = False

    class Settings:
        name = "prompt_versions"
        indexes = [
            "name",
            "version"
        ]
