from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.scout import SavedLead, Business
from app.models.analytics import Goal, AnalyticsEvent
from app.schemas.analytics import GoalCreate, GoalUpdate
from datetime import datetime

class AnalyticsService:
    @staticmethod
    def get_dashboard_metrics(db: Session, user_id: str):
        # We fetch the high level stats for the dashboard by grouping leads
        leads = db.query(SavedLead.status, func.count(SavedLead.id)).filter(SavedLead.user_id == user_id).group_by(SavedLead.status).all()
        status_map = {k: v for k, v in leads}
        
        total = sum(status_map.values())
        contacted = status_map.get('Contacted', 0) + status_map.get('Replied', 0) + status_map.get('Interested', 0) + status_map.get('Meeting Scheduled', 0) + status_map.get('Proposal Sent', 0) + status_map.get('Negotiation', 0) + status_map.get('Won', 0)
        
        replies = status_map.get('Replied', 0) + status_map.get('Interested', 0) + status_map.get('Meeting Scheduled', 0) + status_map.get('Proposal Sent', 0) + status_map.get('Negotiation', 0) + status_map.get('Won', 0)
        
        won = status_map.get('Won', 0)
        conversion = (won / total * 100) if total > 0 else 0
        
        # Simplified revenue for now (would join with a deals/contract table)
        # Using 5000 as an arbitrary Average Deal Size for mockup
        avg_deal_size = 5000 
        
        return {
            "total_leads": total,
            "contacted": contacted,
            "replies": replies,
            "meetings": status_map.get('Meeting Scheduled', 0),
            "proposals_sent": status_map.get('Proposal Sent', 0),
            "deals_won": won,
            "lost_deals": status_map.get('Lost', 0),
            "conversion_rate": round(conversion, 2),
            "expected_revenue": total * avg_deal_size * 0.1, # Mock expectation
            "closed_revenue": won * avg_deal_size
        }

class GoalService:
    @staticmethod
    def get_goals(db: Session, user_id: str):
        return db.query(Goal).filter(Goal.user_id == user_id).all()
        
    @staticmethod
    def create_goal(db: Session, user_id: str, goal_in: GoalCreate):
        goal = Goal(
            user_id=user_id,
            title=goal_in.title,
            type=goal_in.type,
            target_value=goal_in.target_value,
            start_date=goal_in.start_date,
            end_date=goal_in.end_date
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal
        
    @staticmethod
    def update_goal(db: Session, goal_id: str, user_id: str, goal_in: GoalUpdate):
        goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()
        if not goal:
            raise ValueError("Goal not found")
            
        if goal_in.current_value is not None:
            goal.current_value = goal_in.current_value
            if goal.current_value >= goal.target_value:
                goal.status = "completed"
        if goal_in.status is not None:
            goal.status = goal_in.status
            
        db.commit()
        db.refresh(goal)
        return goal

    @staticmethod
    def delete_goal(db: Session, goal_id: str, user_id: str):
        goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()
        if not goal:
            raise ValueError("Goal not found")
        db.delete(goal)
        db.commit()
        return True
