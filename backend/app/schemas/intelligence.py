from pydantic import BaseModel, Field
from typing import List, Dict, Any
from uuid import UUID

class OpportunityReasonSchema(BaseModel):
    reason: str = Field(description="The reason for the score")
    impact: str = Field(description="Impact: 'positive', 'negative', or 'neutral'")

class OpportunityScoreSchema(BaseModel):
    score: int = Field(description="Opportunity score between 0 and 100", ge=0, le=100)
    reasons: List[OpportunityReasonSchema] = Field(description="List of reasons for the score")
    explanation: str = Field(description="Detailed explanation of the score")

class RecommendationSchema(BaseModel):
    service_name: str = Field(description="Name of the recommended service (e.g. 'SEO', 'Website Redesign')")
    reasoning: str = Field(description="Reasoning for this recommendation based on business context")
    estimated_impact: str = Field(description="'High', 'Medium', or 'Low'")
    estimated_effort: str = Field(description="'High', 'Medium', or 'Low'")

class IntelligenceReportSchema(BaseModel):
    executive_summary: str = Field(description="A concise executive summary of the business")
    detailed_summary: str = Field(description="A detailed summary of the business operations, products/services, and value proposition")
    business_category: str = Field(description="The specific category of the business (e.g., 'Boutique Coffee Shop')")
    industry: str = Field(description="The broader industry (e.g., 'Food & Beverage')")
    business_size: str = Field(description="Estimated size (e.g., 'Small (1-10 employees)')")
    target_audience: str = Field(description="Description of their target audience")
    
    digital_maturity: str = Field(description="'Low', 'Medium', or 'High'")
    website_quality: str = Field(description="'Poor', 'Average', 'Good', or 'Excellent'")
    brand_quality: str = Field(description="'Poor', 'Average', 'Good', or 'Excellent'")
    seo_quality: str = Field(description="'Poor', 'Average', 'Good', or 'Excellent'")
    technology_maturity: str = Field(description="'Low', 'Medium', or 'High'")
    online_presence: str = Field(description="'Weak', 'Moderate', or 'Strong'")
    estimated_marketing_maturity: str = Field(description="'Low', 'Medium', or 'High'")
    
    estimated_budget_range: str = Field(description="Estimated budget range (e.g., '$1k-$5k', '$10k+')")
    growth_potential: str = Field(description="'Low', 'Medium', or 'High'")
    decision_maker_guess: str = Field(description="Likely title of the decision maker (e.g., 'Owner', 'Marketing Director')")
    estimated_project_value: str = Field(description="Estimated value of potential project in USD")
    sales_difficulty: str = Field(description="'Easy', 'Medium', or 'Hard'")
    
    strengths: List[str] = Field(description="List of business strengths")
    weaknesses: List[str] = Field(description="List of business weaknesses")
    opportunities: List[str] = Field(description="List of external opportunities")
    risks: List[str] = Field(description="List of risks associated with this business")
    
    next_best_action: str = Field(description="The next best action to take for outreach")
    
    opportunity_score: OpportunityScoreSchema = Field(description="Opportunity score and reasoning")
    recommendations: List[RecommendationSchema] = Field(description="List of recommended services")
    ai_tags: List[str] = Field(description="List of relevant tags (e.g., 'High Budget', 'Weak SEO')")
    
    ai_confidence: float = Field(description="Confidence in the analysis (0.0 to 1.0)", ge=0.0, le=1.0)

class IntelligenceReportResponse(BaseModel):
    id: UUID
    business_id: UUID
    report: IntelligenceReportSchema
    created_at: str

class AnalyzeRequest(BaseModel):
    business_id: UUID
    force_reanalyze: bool = False
