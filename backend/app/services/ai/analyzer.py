import time
from sqlalchemy.orm import Session
from app.models.scout import Business, BusinessAnalysis
from app.schemas.ai import AIAnalysisResult
from app.services.ai.provider import BaseAIProvider
from app.services.ai.prompts import PromptManager

class AIService:
    def __init__(self, provider: BaseAIProvider, db: Session):
        self.provider = provider
        self.db = db

    def analyze_business(self, business_id: str, force_reanalyze: bool = False) -> BusinessAnalysis:
        # Check if already analyzed
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            raise ValueError("Business not found")

        existing_analysis = self.db.query(BusinessAnalysis).filter(BusinessAnalysis.business_id == business_id).first()
        if existing_analysis and not force_reanalyze:
            return existing_analysis

        # Prepare Data
        b_data = {
            "business_name": business.business_name,
            "category": business.category,
            "website": business.website,
            "phone": business.phone,
            "email": business.email,
            "google_rating": business.google_rating,
            "review_count": business.review_count,
            "city": business.city,
            "state": business.state,
            "country": business.country,
            "website_status": business.website_status,
            "confidence_score": business.confidence_score,
        }

        prompt = PromptManager.build_analysis_prompt(b_data)

        # Retry logic for structured generation
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                result_schema: AIAnalysisResult = self.provider.generate_structured(prompt, AIAnalysisResult)
                
                # Save to DB
                if existing_analysis:
                    analysis = existing_analysis
                else:
                    analysis = BusinessAnalysis(business_id=business_id)
                    
                analysis.summary_short = result_schema.summary_short
                analysis.summary_medium = result_schema.summary_medium
                analysis.summary_long = result_schema.summary_long
                analysis.strengths = result_schema.strengths
                analysis.weaknesses = result_schema.weaknesses
                analysis.opportunities = result_schema.opportunities
                analysis.opportunity_score = result_schema.opportunity_score
                analysis.confidence_score = result_schema.confidence_score
                analysis.ai_tags = result_schema.ai_tags
                analysis.estimated_budget = result_schema.estimated_budget
                analysis.recommended_services = result_schema.recommended_services

                if not existing_analysis:
                    self.db.add(analysis)
                    
                self.db.commit()
                self.db.refresh(analysis)
                return analysis
                
            except Exception as e:
                last_error = e
                time.sleep(1) # wait before retry
                
        raise RuntimeError(f"Failed to analyze business after {max_retries} attempts. Last error: {str(last_error)}")
