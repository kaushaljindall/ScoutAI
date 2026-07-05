from sqlalchemy.orm import Session
from app.models.scout import SavedLead
from app.models.crm import Conversation, Task
from app.schemas.crm import ConversationCreate, TaskCreate, TaskUpdate
from app.services.crm.timeline import TimelineService

class CRMService:
    @staticmethod
    def update_status(db: Session, lead_id: str, new_status: str, user_id: str):
        lead = db.query(SavedLead).filter(SavedLead.id == lead_id, SavedLead.user_id == user_id).first()
        if not lead:
            raise ValueError("Lead not found")
        
        old_status = lead.status
        lead.status = new_status
        db.commit()
        
        TimelineService.log_event(db, lead_id, "Status Change", f"Moved from {old_status} to {new_status}")
        return lead

class ConversationService:
    @staticmethod
    def add_conversation(db: Session, lead_id: str, conv_in: ConversationCreate, user_id: str):
        # Optional: verify lead belongs to user
        conv = Conversation(
            lead_id=lead_id,
            type=conv_in.type,
            message=conv_in.message,
            sender=conv_in.sender
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        
        TimelineService.log_event(db, lead_id, "Conversation", f"Logged {conv_in.type} from {conv_in.sender}")
        return conv

    @staticmethod
    def get_conversations(db: Session, lead_id: str):
        return db.query(Conversation).filter(Conversation.lead_id == lead_id).order_by(Conversation.created_at.desc()).all()

class TaskService:
    @staticmethod
    def create_task(db: Session, lead_id: str, task_in: TaskCreate, user_id: str):
        task = Task(
            lead_id=lead_id,
            title=task_in.title,
            due_date=task_in.due_date,
            type=task_in.type
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        TimelineService.log_event(db, lead_id, "Task Created", f"Task: {task_in.title}")
        return task

    @staticmethod
    def get_tasks(db: Session, user_id: str, lead_id: str = None):
        query = db.query(Task).join(SavedLead).filter(SavedLead.user_id == user_id)
        if lead_id:
            query = query.filter(Task.lead_id == lead_id)
        return query.order_by(Task.due_date.asc()).all()

    @staticmethod
    def update_task(db: Session, task_id: str, task_in: TaskUpdate):
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError("Task not found")
            
        if task_in.completed is not None:
            task.completed = task_in.completed
            TimelineService.log_event(db, str(task.lead_id), "Task Completed", f"Task completed: {task.title}")
            
        db.commit()
        db.refresh(task)
        return task
