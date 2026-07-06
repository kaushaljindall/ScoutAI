from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.models.agent import ExecutionState

class PlanRequest(BaseModel):
    query: str = Field(..., example="Find dentists in Chandigarh with outdated websites.")

class PlanResponse(BaseModel):
    intent: str
    industry: Optional[str] = None
    location: Optional[str] = None
    requires: List[str] = Field(default_factory=list)

class ExecuteRequest(BaseModel):
    session_id: UUID
    plan: PlanResponse

class ToolInvocationSchema(BaseModel):
    id: UUID
    tool_name: str
    input_params: Optional[Dict[str, Any]]
    output_result: Optional[Dict[str, Any]]
    error: Optional[str]
    execution_time: Optional[float]
    status: ExecutionState

    model_config = {"from_attributes": True}

class ExecutionLogSchema(BaseModel):
    id: UUID
    level: str
    message: str
    details: Optional[Dict[str, Any]]
    timestamp: datetime

    model_config = {"from_attributes": True}

class AgentExecutionSchema(BaseModel):
    id: UUID
    agent_name: str
    status: ExecutionState
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    tool_invocations: List[ToolInvocationSchema] = Field(default_factory=list)
    logs: List[ExecutionLogSchema] = Field(default_factory=list)

    model_config = {"from_attributes": True}

class SearchSessionSchema(BaseModel):
    id: UUID
    user_id: str
    original_query: str
    planner_output: Optional[Dict[str, Any]]
    execution_time: Optional[float]
    status: ExecutionState
    errors: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    executions: List[AgentExecutionSchema] = Field(default_factory=list)

    model_config = {"from_attributes": True}
