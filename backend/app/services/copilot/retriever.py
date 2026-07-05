from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.scout import SavedLead, Business, BusinessAnalysis
from app.models.crm import Task, Conversation
from datetime import datetime

class WorkspaceRetriever:
    def __init__(self, db: Session):
        self.db = db

    def get_global_context(self, user_id: str):
        # A lightweight summary of the user's workspace
        total_leads = self.db.query(SavedLead).filter(SavedLead.user_id == user_id).count()
        
        now = datetime.utcnow()
        overdue_tasks = self.db.query(Task).join(SavedLead).filter(
            SavedLead.user_id == user_id, 
            Task.completed == False, 
            Task.due_date < now
        ).count()
        
        high_opp = self.db.query(SavedLead).join(Business).join(BusinessAnalysis).filter(
            SavedLead.user_id == user_id,
            BusinessAnalysis.opportunity_score >= 85
        ).count()
        
        # Determine leads that haven't been replied to recently (simplification)
        return {
            "total_leads": total_leads,
            "overdue_tasks": overdue_tasks,
            "high_opportunity_leads": high_opp,
        }

    def get_lead_context(self, user_id: str, lead_id: str):
        lead = self.db.query(SavedLead).filter(SavedLead.id == lead_id, SavedLead.user_id == user_id).first()
        if not lead:
            return None
            
        business = self.db.query(Business).filter(Business.id == lead.business_id).first()
        analysis = self.db.query(BusinessAnalysis).filter(BusinessAnalysis.business_id == lead.business_id).first()
        tasks = self.db.query(Task).filter(Task.lead_id == lead_id, Task.completed == False).all()
        
        return {
            "status": lead.status,
            "business_name": business.business_name if business else None,
            "industry": business.category if business else None,
            "opportunity_score": analysis.opportunity_score if analysis else None,
            "strengths": analysis.strengths if analysis else [],
            "weaknesses": analysis.weaknesses if analysis else [],
            "pending_tasks": [t.title for t in tasks]
        }
