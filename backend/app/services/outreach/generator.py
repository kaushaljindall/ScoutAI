import time
from sqlalchemy.orm import Session
from app.models.scout import Business, BusinessAnalysis
from app.models.outreach import GeneratedMessage
from app.schemas.outreach import MessageGenerationRequest, MessageVariation
from app.services.ai.provider import BaseAIProvider
from app.services.outreach.prompts import OutreachPromptManager
import json

class OutreachService:
    def __init__(self, provider: BaseAIProvider, db: Session):
        self.provider = provider
        self.db = db

    def generate_variations(self, business_id: str, request: MessageGenerationRequest) -> list[MessageVariation]:
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            raise ValueError("Business not found")
            
        analysis = self.db.query(BusinessAnalysis).filter(BusinessAnalysis.business_id == business_id).first()
        if not analysis:
            raise ValueError("Business analysis not found. Please analyze the business first.")

        b_data = {
            "business_name": business.business_name,
            "category": business.category,
            "website": business.website,
            "phone": business.phone,
            "email": business.email,
        }
        
        a_data = {
            "summary_short": analysis.summary_short,
            "strengths": analysis.strengths,
            "opportunities": analysis.opportunities,
        }
        
        req_params = request.model_dump()
        variations = []
        
        for version in ["A", "B", "C"]:
            prompt = OutreachPromptManager.get_system_prompt() + "\n" + OutreachPromptManager.build_message_prompt(
                b_data, a_data, req_params, version
            )
            
            # Request structured output via Gemini
            try:
                # Assuming the schema allows returning the MessageVariation structure directly
                result: MessageVariation = self.provider.generate_structured(prompt, MessageVariation)
                
                # Format full message based on pieces
                if not getattr(result, "full_message", None):
                    result.full_message = f"{result.structured_content.opening}\n\n{result.structured_content.observation}\n\n{result.structured_content.value_proposition}\n\n{result.structured_content.cta}\n\n{result.structured_content.closing}"
                
                # Override version explicitly
                result.version = f"Version {version}"
                
                # Save to DB
                gm = GeneratedMessage(
                    business_id=business_id,
                    message_type=request.message_type,
                    tone=request.tone,
                    language=request.language,
                    ai_version=result.version,
                    opening=result.structured_content.opening,
                    observation=result.structured_content.observation,
                    value_proposition=result.structured_content.value_proposition,
                    cta=result.structured_content.cta,
                    closing=result.structured_content.closing,
                    full_message=result.full_message,
                    ai_suggestions=result.ai_suggestions.model_dump() if result.ai_suggestions else {}
                )
                self.db.add(gm)
                variations.append(result)
            except Exception as e:
                # Optionally handle failure gracefully
                continue
                
        self.db.commit()
        
        if not variations:
            raise RuntimeError("Failed to generate message variations. Please try again.")
            
        return variations
