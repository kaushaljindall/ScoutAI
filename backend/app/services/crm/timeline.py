from sqlalchemy.orm import Session
from app.models.crm import TimelineEvent

class TimelineService:
    @staticmethod
    def log_event(db: Session, lead_id: str, event_type: str, description: str, metadata: dict = None):
        event = TimelineEvent(
            lead_id=lead_id,
            event_type=event_type,
            description=description,
            metadata_json=metadata or {}
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_timeline(db: Session, lead_id: str):
        return db.query(TimelineEvent).filter(TimelineEvent.lead_id == lead_id).order_by(TimelineEvent.created_at.desc()).all()
