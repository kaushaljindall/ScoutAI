import asyncio
from app.models.scout import Business, BusinessAnalysis
from app.schemas.ai import AIAnalysisResult
from app.services.ai.provider import BaseAIProvider
from app.services.ai.prompts import PromptManager

class AIService:
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider

    async def analyze_business(self, business_id: str, force_reanalyze: bool = False) -> BusinessAnalysis:
        # Check if already analyzed
        business = await Business.get(business_id)
        if not business:
            raise ValueError("Business not found")

        existing_analysis = await BusinessAnalysis.find_one(BusinessAnalysis.business_id == business_id)
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
                # generate_structured is synchronous in the provider
                def generate():
                    return self.provider.generate_structured(prompt, AIAnalysisResult)
                
                result_schema: AIAnalysisResult = await asyncio.to_thread(generate)
                
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

                await analysis.save() if existing_analysis else await analysis.insert()
                return analysis
                
            except Exception as e:
                last_error = e
                await asyncio.sleep(1) # wait before retry
                
        raise RuntimeError(f"Failed to analyze business after {max_retries} attempts. Last error: {str(last_error)}")

    async def analyze(self, business: Business) -> dict:
        """Analyze a business instance directly and return dictionary data"""
        b_data = {
            "business_name": business.business_name,
            "website": business.website,
            "phone": business.phone,
            "email": business.email,
            "raw_text": business.raw_data.get("scraped_text", "") if business.raw_data else ""
        }

        prompt = PromptManager.build_analysis_prompt(b_data)
        
        def generate():
            return self.provider.generate_structured(prompt, AIAnalysisResult)
            
        result_schema: AIAnalysisResult = await asyncio.to_thread(generate)
        
        return {
            "summary_short": result_schema.summary_short,
            "summary_medium": result_schema.summary_medium,
            "summary_long": result_schema.summary_long,
            "strengths": result_schema.strengths,
            "weaknesses": result_schema.weaknesses,
            "opportunities": result_schema.opportunities,
            "opportunity_score": result_schema.opportunity_score,
            "confidence_score": result_schema.confidence_score,
            "ai_tags": result_schema.ai_tags,
            "estimated_budget": result_schema.estimated_budget,
            "recommended_services": result_schema.recommended_services
        }
