from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.api.deps import SessionDep, CurrentUser
from app.schemas.analytics import (
    GoalCreate, GoalUpdate, GoalResponse, DashboardMetricsResponse, AIInsightResponse
)
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.services.analytics.manager import AnalyticsService, GoalService
from app.services.analytics.engine import InsightEngine

router = APIRouter()

def get_engine(db: SessionDep):
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
    return InsightEngine(provider=provider, db=db)

# --- Dashboard & Metrics ---
@router.get("/dashboard", response_model=DashboardMetricsResponse)
def get_dashboard(db: SessionDep, current_user: CurrentUser):
    return AnalyticsService.get_dashboard_metrics(db, str(current_user.id))

# --- AI Insights ---
@router.get("/insights", response_model=List[AIInsightResponse])
def get_insights(db: SessionDep, current_user: CurrentUser):
    engine = get_engine(db)
    try:
        return engine.generate_insights(str(current_user.id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Goals ---
@router.get("/goals", response_model=List[GoalResponse])
def get_goals(db: SessionDep, current_user: CurrentUser):
    return GoalService.get_goals(db, str(current_user.id))

@router.post("/goals", response_model=GoalResponse)
def create_goal(goal_in: GoalCreate, db: SessionDep, current_user: CurrentUser):
    return GoalService.create_goal(db, str(current_user.id), goal_in)

@router.put("/goals/{id}", response_model=GoalResponse)
def update_goal(id: str, goal_in: GoalUpdate, db: SessionDep, current_user: CurrentUser):
    try:
        return GoalService.update_goal(db, id, str(current_user.id), goal_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Goal not found")

@router.delete("/goals/{id}")
def delete_goal(id: str, db: SessionDep, current_user: CurrentUser):
    try:
        GoalService.delete_goal(db, id, str(current_user.id))
        return {"status": "success"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Goal not found")
