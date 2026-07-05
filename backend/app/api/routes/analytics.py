from fastapi import APIRouter, HTTPException
from typing import List, Any
from app.api.deps import CurrentUser
from app.schemas.analytics import (
    GoalCreate, GoalUpdate, GoalResponse, DashboardMetricsResponse, AIInsightResponse
)
from app.models.analytics import Goal, AnalyticsEvent
from app.models.scout import SavedLead

router = APIRouter()

@router.get("/dashboard", response_model=DashboardMetricsResponse)
async def get_dashboard(current_user: CurrentUser):
    user_id = str(current_user.id)
    total_leads = await SavedLead.find(SavedLead.user_id == user_id, SavedLead.is_deleted == False).count()
    contacted = await SavedLead.find(SavedLead.user_id == user_id, SavedLead.status == "contacted").count()
    converted = await SavedLead.find(SavedLead.user_id == user_id, SavedLead.status == "converted").count()
    goals = await Goal.find(Goal.user_id == user_id, Goal.status == "active").count()

    return {
        "total_leads": total_leads,
        "leads_contacted": contacted,
        "leads_converted": converted,
        "active_goals": goals,
        "conversion_rate": round((converted / total_leads * 100) if total_leads > 0 else 0, 1),
    }

@router.get("/insights", response_model=List[AIInsightResponse])
async def get_insights(current_user: CurrentUser):
    # Return basic insights without AI for now
    return [
        {"title": "Lead Activity", "insight": "You have active leads in your pipeline.", "type": "info"},
    ]

@router.get("/goals", response_model=List[GoalResponse])
async def get_goals(current_user: CurrentUser):
    return await Goal.find(
        Goal.user_id == str(current_user.id),
        Goal.is_deleted == False
    ).to_list()

@router.post("/goals", response_model=GoalResponse)
async def create_goal(goal_in: GoalCreate, current_user: CurrentUser):
    goal = Goal(user_id=str(current_user.id), **goal_in.model_dump())
    await goal.insert()
    return goal

@router.put("/goals/{id}", response_model=GoalResponse)
async def update_goal(id: str, goal_in: GoalUpdate, current_user: CurrentUser):
    goal = await Goal.find_one(Goal.id == id, Goal.user_id == str(current_user.id))
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for k, v in goal_in.model_dump(exclude_unset=True).items():
        setattr(goal, k, v)
    await goal.save()
    return goal

@router.delete("/goals/{id}")
async def delete_goal(id: str, current_user: CurrentUser):
    goal = await Goal.find_one(Goal.id == id, Goal.user_id == str(current_user.id))
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    goal.is_deleted = True
    await goal.save()
    return {"status": "success"}
