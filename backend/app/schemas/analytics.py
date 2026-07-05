from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any, Dict
from uuid import UUID
from datetime import datetime

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
    id: UUID
    user_id: UUID
    current_value: float
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReportBase(BaseModel):
    type: str
    date_range: str

class ReportResponse(ReportBase):
    id: UUID
    user_id: UUID
    insights: Dict[str, Any]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class DashboardMetricsResponse(BaseModel):
    total_leads: int
    contacted: int
    replies: int
    meetings: int
    proposals_sent: int
    deals_won: int
    lost_deals: int
    conversion_rate: float
    expected_revenue: float
    closed_revenue: float

class AIInsightResponse(BaseModel):
    insight: str
    explanation: str
    action_type: str
