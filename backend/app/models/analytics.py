from typing import Optional
from datetime import datetime
from beanie import Indexed
from app.models.base import BaseDocument


class Goal(BaseDocument):
    user_id: Indexed(str)
    title: str
    type: str  # revenue, contacts, deals, follow_ups
    target_value: float
    current_value: float = 0.0
    start_date: datetime
    end_date: datetime
    status: str = "active"  # active, completed, failed

    class Settings:
        name = "goals"


class AnalyticsEvent(BaseDocument):
    user_id: Indexed(str)
    event_type: Indexed(str)
    event_data: dict = {}

    class Settings:
        name = "analytics_events"


class Report(BaseDocument):
    user_id: Indexed(str)
    type: str  # weekly, monthly, quarterly
    insights: dict
    date_range: str

    class Settings:
        name = "reports"
