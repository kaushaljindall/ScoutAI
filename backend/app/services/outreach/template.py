from sqlalchemy.orm import Session
from app.models.outreach import MessageTemplate
from app.schemas.outreach import MessageTemplateBase
import uuid

class TemplateService:
    def __init__(self, db: Session):
        self.db = db

    def get_templates(self, user_id: str):
        return self.db.query(MessageTemplate).filter(MessageTemplate.user_id == user_id).all()

    def create_template(self, user_id: str, template_in: MessageTemplateBase):
        template = MessageTemplate(
            user_id=user_id,
            title=template_in.title,
            type=template_in.type,
            tone=template_in.tone,
            language=template_in.language,
            template=template_in.template,
            is_favorite=template_in.is_favorite
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def update_template(self, id: str, user_id: str, template_in: MessageTemplateBase):
        template = self.db.query(MessageTemplate).filter(MessageTemplate.id == id, MessageTemplate.user_id == user_id).first()
        if not template:
            raise ValueError("Template not found")
            
        for key, value in template_in.model_dump().items():
            setattr(template, key, value)
            
        self.db.commit()
        self.db.refresh(template)
        return template

    def delete_template(self, id: str, user_id: str):
        template = self.db.query(MessageTemplate).filter(MessageTemplate.id == id, MessageTemplate.user_id == user_id).first()
        if not template:
            raise ValueError("Template not found")
            
        self.db.delete(template)
        self.db.commit()
        return True
