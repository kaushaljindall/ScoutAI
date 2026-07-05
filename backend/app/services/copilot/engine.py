from sqlalchemy.orm import Session
from app.services.ai.provider import BaseAIProvider
from app.services.copilot.manager import ChatRepository, PreferenceService
from app.services.copilot.retriever import WorkspaceRetriever
from app.schemas.copilot import CopilotChatRequest, CopilotChatResponse, AIMessageResponse
from pydantic import BaseModel
import json

class PromptBuilder:
    @staticmethod
    def build(message: str, global_context: dict, local_context: dict = None, history: list = None) -> str:
        sys = "You are the ScoutAI Copilot, an intelligent AI business assistant that understands the user's entire CRM workspace. Do not expose internal IDs. Be concise and actionable."
        
        context_str = f"Global Workspace State:\nTotal Leads: {global_context.get('total_leads')}\nOverdue Tasks: {global_context.get('overdue_tasks')}\nHigh Opportunity Leads: {global_context.get('high_opportunity_leads')}\n\n"
        
        if local_context:
            context_str += f"Current Lead Focus: {local_context.get('business_name')} ({local_context.get('industry')})\nStatus: {local_context.get('status')}\nOpportunity Score: {local_context.get('opportunity_score')}\nPending Tasks: {', '.join(local_context.get('pending_tasks', []))}\n\n"
            
        hist_str = ""
        if history:
            hist_str = "Recent Chat History:\n"
            for msg in history[-4:]: # last 4 messages
                hist_str += f"{msg.role.capitalize()}: {msg.message}\n"
                
        return f"{sys}\n\n{context_str}\n{hist_str}\nUser: {message}\nAssistant:"

class CopilotStructuredResponse(BaseModel):
    message: str
    suggested_actions: list[str]

class ContextEngine:
    def __init__(self, provider: BaseAIProvider, db: Session):
        self.provider = provider
        self.db = db
        self.repo = ChatRepository(db)
        self.retriever = WorkspaceRetriever(db)
        self.prefs = PreferenceService(db)

    def process_chat(self, user_id: str, request: CopilotChatRequest):
        chat = self.repo.get_or_create_chat(user_id, str(request.chat_id) if request.chat_id else None)
        
        # Add user message
        self.repo.add_message(str(chat.id), "user", request.message)
        
        # Gather Context
        global_ctx = self.retriever.get_global_context(user_id)
        local_ctx = None
        if request.current_context and request.current_context.get("lead_id"):
            local_ctx = self.retriever.get_lead_context(user_id, request.current_context.get("lead_id"))
            
        history = self.repo.get_chat_history(str(chat.id))
        
        # Build prompt
        prompt = PromptBuilder.build(request.message, global_ctx, local_ctx, history[:-1])
        
        try:
            result: CopilotStructuredResponse = self.provider.generate_structured(prompt, CopilotStructuredResponse)
            
            # Save assistant message
            context_used = {"global": global_ctx, "local": local_ctx}
            ai_msg = self.repo.add_message(str(chat.id), "assistant", result.message, context_used)
            
            return {
                "chat_id": chat.id,
                "message": AIMessageResponse.model_validate(ai_msg),
                "suggested_actions": result.suggested_actions
            }
        except Exception as e:
            raise RuntimeError(f"Copilot generation failed: {str(e)}")
