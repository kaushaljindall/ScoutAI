from sqlalchemy.orm import Session
from app.services.ai.provider import BaseAIProvider
from app.services.copilot.retriever import WorkspaceRetriever
from pydantic import BaseModel

class DocumentGenerationOutput(BaseModel):
    title: str
    content: str # Markdown

class DocumentGenerator:
    def __init__(self, provider: BaseAIProvider, db: Session):
        self.provider = provider
        self.db = db
        self.retriever = WorkspaceRetriever(db)

    def generate(self, user_id: str, lead_id: str, doc_type: str, custom_context: dict = None) -> DocumentGenerationOutput:
        lead_ctx = self.retriever.get_lead_context(user_id, lead_id)
        if not lead_ctx:
            raise ValueError("Lead not found or lacks context")

        # Select prompt template based on document type
        if doc_type == 'proposal':
            sys_prompt = "You are an expert sales consultant writing a high-converting proposal in Markdown format."
            instructions = """
            Include these sections:
            # Executive Summary
            # Current Problems
            # Proposed Solution
            # Project Scope
            # Timeline
            # Deliverables
            # Pricing (Leave generic [AMOUNT] if unknown)
            # Next Steps
            """
        elif doc_type == 'quotation':
            sys_prompt = "You are a professional accountant generating a quotation in Markdown."
            instructions = "Generate a table with columns: Service Name, Description, Quantity, Unit Cost, Subtotal. Add a final Total."
        elif doc_type == 'scope':
            sys_prompt = "You are a technical project manager writing a Scope of Work (SOW) in Markdown."
            instructions = "Include: Objectives, Features, Deliverables, Timeline, Assumptions, Client Responsibilities."
        elif doc_type == 'contract':
            sys_prompt = "You are a legal assistant generating a standard freelance project contract in Markdown."
            instructions = "Include standard clauses for payment, revisions, intellectual property, and termination."
        elif doc_type == 'meeting-summary':
            sys_prompt = "You are an AI assistant summarizing a meeting in Markdown."
            instructions = "Include: Meeting Summary, Action Items, Decisions Made."
        else:
            raise ValueError("Unsupported document type")

        business_data = f"""
        Business: {lead_ctx.get('business_name')} ({lead_ctx.get('industry')})
        Status: {lead_ctx.get('status')}
        Pain Points / Weaknesses: {', '.join(lead_ctx.get('weaknesses', []))}
        Strengths: {', '.join(lead_ctx.get('strengths', []))}
        """

        prompt = f"""
        {sys_prompt}
        
        Using the following context, write the document.
        {business_data}
        
        {f"Additional Context: {custom_context}" if custom_context else ""}
        
        {instructions}
        
        Output MUST be in Markdown format. Return JSON containing the title and the markdown content.
        """

        try:
            return self.provider.generate_structured(prompt, DocumentGenerationOutput)
        except Exception as e:
            raise RuntimeError(f"Document generation failed: {str(e)}")
