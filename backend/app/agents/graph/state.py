from typing import TypedDict, List, Dict, Any, Optional
from uuid import UUID
from app.schemas.agent import PlanResponse
from app.models.agent import ExecutionState

class GraphState(TypedDict):
    session_id: UUID
    query: str
    plan: Optional[PlanResponse]
    tools_selected: List[str]
    tool_results: List[Dict[str, Any]]
    current_status: ExecutionState
    errors: List[str]
