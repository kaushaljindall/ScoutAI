from pydantic import BaseModel, ConfigDict, BeforeValidator
from typing import List, Optional, Any, Dict, Annotated
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class GoalBase(BaseModel):
    title: str
    type: str
    target_value: float
    start_date: datetime
    end_date: datetime

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    current_value: Optional[float] = None
    status: Optional[str] = None

class GoalResponse(GoalBase):
    id: PyObjectId
    user_id: PyObjectId
    current_value: float
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class ReportResponse(BaseModel):
    id: PyObjectId
    user_id: PyObjectId
    type: str
    date_range: str
    insights: Dict[str, Any]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class DashboardMetricsResponse(BaseModel):
    total_leads: int
    leads_contacted: int
    leads_converted: int
    active_goals: int
    conversion_rate: float

class AIInsightResponse(BaseModel):
    title: str
    insight: str
    type: str
