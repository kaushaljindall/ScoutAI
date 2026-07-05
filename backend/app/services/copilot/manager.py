from sqlalchemy.orm import Session
from app.models.copilot import AIChat, AIMessage, UserPreference
from app.schemas.copilot import UserPreferenceBase
import uuid

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_chat(self, user_id: str, chat_id: str = None) -> AIChat:
        if chat_id:
            chat = self.db.query(AIChat).filter(AIChat.id == chat_id, AIChat.user_id == user_id).first()
            if chat:
                return chat
        
        chat = AIChat(user_id=user_id, title="Workspace Copilot Chat")
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def add_message(self, chat_id: str, role: str, message: str, context_used: dict = None) -> AIMessage:
        msg = AIMessage(
            chat_id=chat_id,
            role=role,
            message=message,
            context_used=context_used or {}
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg
        
    def get_chat_history(self, chat_id: str):
        return self.db.query(AIMessage).filter(AIMessage.chat_id == chat_id).order_by(AIMessage.created_at.asc()).all()

    def get_user_chats(self, user_id: str):
        return self.db.query(AIChat).filter(AIChat.user_id == user_id).order_by(AIChat.created_at.desc()).all()

class PreferenceService:
    def __init__(self, db: Session):
        self.db = db

    def get_preferences(self, user_id: str) -> UserPreference:
        pref = self.db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
        if not pref:
            pref = UserPreference(user_id=user_id)
            self.db.add(pref)
            self.db.commit()
            self.db.refresh(pref)
        return pref

    def update_preferences(self, user_id: str, prefs_in: UserPreferenceBase) -> UserPreference:
        pref = self.get_preferences(user_id)
        for key, value in prefs_in.model_dump(exclude_unset=True).items():
            setattr(pref, key, value)
        self.db.commit()
        self.db.refresh(pref)
        return pref
