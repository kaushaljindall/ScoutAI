from sqlalchemy.orm import Session
from app.models.crm import Conversation, AIConversationAnalysis
from app.services.ai.provider import BaseAIProvider
from pydantic import BaseModel
from typing import List, Optional

class AIConversationAnalysisOutput(BaseModel):
    summary: str
    sentiment: str
    interest_level: str
    objections: List[str]
    buying_intent: str
    next_action: str
    confidence_score: float

class AIConversationService:
    def __init__(self, provider: BaseAIProvider, db: Session):
        self.provider = provider
        self.db = db

    def analyze_conversation(self, conversation_id: str) -> AIConversationAnalysis:
        conversation = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise ValueError("Conversation not found")

        # Basic Prompt for Analysis
        prompt = f"""
        Analyze the following conversation message and provide structured intelligence.
        Message: "{conversation.message}"
        Sender: {conversation.sender}
        
        Extract the following:
        - summary: A 1-sentence summary
        - sentiment: Positive, Neutral, or Negative
        - interest_level: High, Medium, Low
        - objections: Array of objections or concerns raised (if any)
        - buying_intent: High, Medium, Low, None
        - next_action: Recommended next step
        - confidence_score: Float between 0 and 1
        """

        result: AIConversationAnalysisOutput = self.provider.generate_structured(prompt, AIConversationAnalysisOutput)
        
        analysis = AIConversationAnalysis(
            conversation_id=conversation_id,
            summary=result.summary,
            sentiment=result.sentiment,
            interest_level=result.interest_level,
            objections=result.objections,
            buying_intent=result.buying_intent,
            next_action=result.next_action,
            confidence_score=result.confidence_score
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

class ReplySuggestions(BaseModel):
    replies: List[str]
    best_follow_up_date: str
    suggested_channel: str
    reason: str

class ReplyGenerationService:
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider

    def generate_replies(self, context: str) -> ReplySuggestions:
        prompt = f"""
        You are an expert sales consultant. A client has sent the following message/context:
        "{context}"
        
        Generate 3 distinct reply options (Reply A: Direct, Reply B: Consultative, Reply C: Soft/Friendly).
        Also recommend the best follow-up date and channel based on context.
        """
        
        return self.provider.generate_structured(prompt, ReplySuggestions)
