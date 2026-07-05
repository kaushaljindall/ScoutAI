from sqlalchemy.orm import Session
from app.services.ai.provider import BaseAIProvider
from app.services.analytics.manager import AnalyticsService
from app.schemas.analytics import AIInsightResponse
from pydantic import BaseModel
from typing import List

class InsightCollectionResponse(BaseModel):
    insights: List[AIInsightResponse]

class InsightEngine:
    def __init__(self, provider: BaseAIProvider, db: Session):
        self.provider = provider
        self.db = db

    def generate_insights(self, user_id: str) -> List[dict]:
        # Fetch high-level stats
        stats = AnalyticsService.get_dashboard_metrics(self.db, user_id)
        
        prompt = f"""
        You are a Senior Data Analyst AI for ScoutAI.
        Analyze the following CRM metrics and provide 3 highly actionable, specific insights.
        Do not just restate the numbers. Calculate hypothetical trends and tell the user what they should focus on.
        
        Metrics:
        - Total Leads: {stats['total_leads']}
        - Contacted: {stats['contacted']}
        - Replies: {stats['replies']}
        - Meetings: {stats['meetings']}
        - Proposals Sent: {stats['proposals_sent']}
        - Deals Won: {stats['deals_won']}
        - Conversion Rate: {stats['conversion_rate']}%
        - Expected Revenue: ${stats['expected_revenue']}
        
        Provide the response exactly matching the schema.
        action_type can be: "warning", "success", or "info".
        """
        
        try:
            result = self.provider.generate_structured(prompt, InsightCollectionResponse)
            return [i.model_dump() for i in result.insights]
        except Exception as e:
            raise RuntimeError(f"Insight generation failed: {str(e)}")
