import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.postgres import get_postgres_session
from app.schemas.agent import (
    PlanRequest, PlanResponse, ExecuteRequest, 
    SearchSessionSchema, AgentExecutionSchema
)
from app.models.agent import SearchSession, ExecutionState
from app.agents.planner.planner import plan_execution
from app.agents.router.router import agent_router
from app.agents.graph.state import GraphState
from app.tools.registry.registry import registry
from app.events.bus import event_bus

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/plan", response_model=PlanResponse)
async def create_plan(request: PlanRequest):
    """Generate an execution plan based on user query."""
    return await plan_execution(request)

@router.post("/execute", response_model=SearchSessionSchema)
async def execute_plan(request: ExecuteRequest, session: AsyncSession = Depends(get_postgres_session)):
    """Execute a plan using the Agent Router."""
    # Create a new search session
    db_session = SearchSession(
        id=request.session_id,
        user_id="system",  # placeholder, would come from auth
        original_query=request.plan.intent,
        planner_output=request.plan.model_dump(),
        status=ExecutionState.PENDING
    )
    session.add(db_session)
    await session.commit()
    await session.refresh(db_session)
    
    # Trigger graph execution
    initial_state = GraphState(
        session_id=request.session_id,
        query=request.plan.intent,
        plan=request.plan,
        tools_selected=[],
        tool_results=[],
        current_status=ExecutionState.PENDING,
        errors=[]
    )
    
    # For production, this should be sent to a background task queue (Celery/ARQ/BackgroundTasks)
    # But for the foundation, we invoke it directly or asynchronously.
    # We will await it here for simplicity, or return pending.
    # To support streaming/tracking, we'll run it and return the final state,
    # or return the initial and let the frontend poll. Let's run it synchronously for the API response in this phase.
    
    try:
        final_state = await agent_router.ainvoke(initial_state)
        
        db_session.status = final_state.get("current_status", ExecutionState.FAILED)
        db_session.errors = final_state.get("errors", [])
        
        await session.commit()
        await session.refresh(db_session)
        
    except Exception as e:
        db_session.status = ExecutionState.FAILED
        db_session.errors = [str(e)]
        await session.commit()
        await session.refresh(db_session)
        
    return db_session

@router.get("/session/{session_id}", response_model=SearchSessionSchema)
async def get_session(session_id: uuid.UUID, session: AsyncSession = Depends(get_postgres_session)):
    """Retrieve a search session by ID."""
    result = await session.execute(select(SearchSession).where(SearchSession.id == session_id))
    db_session = result.scalars().first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

@router.get("/status/{session_id}")
async def get_status(session_id: uuid.UUID, session: AsyncSession = Depends(get_postgres_session)):
    """Get the current status of an execution."""
    result = await session.execute(select(SearchSession).where(SearchSession.id == session_id))
    db_session = result.scalars().first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "status": db_session.status, "errors": db_session.errors}

@router.get("/tools")
async def get_tools():
    """List all registered tools."""
    tools = registry.get_all_tools()
    return [{"name": t.name, "description": t.description} for t in tools]

@router.get("/health")
async def health_check():
    """Check health of the agentic system and tools."""
    tools = registry.get_all_tools()
    health_status = {}
    for t in tools:
        is_healthy = await t.health_check()
        health_status[t.name] = "healthy" if is_healthy else "unhealthy"
    return {"status": "ok", "tools": health_status}
