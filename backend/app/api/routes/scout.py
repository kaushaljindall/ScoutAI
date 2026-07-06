import math
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Response
from app.api.deps import CurrentUser
from app.models.scout import Business, SavedLead
from app.schemas.scout import BusinessResponse, PaginatedBusinesses, SavedLeadCreate, SavedLeadResponse

router = APIRouter()

@router.get("/search", response_model=PaginatedBusinesses)
async def search_businesses(
    current_user: CurrentUser,
    q: Optional[str] = None,
    category: Optional[str] = None,
    city: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
) -> Any:
    filter_query = {"is_deleted": False}
    if q:
        filter_query["$or"] = [
            {"business_name": {"$regex": q, "$options": "i"}},
            {"website": {"$regex": q, "$options": "i"}},
            {"email": {"$regex": q, "$options": "i"}},
        ]
    if category:
        filter_query["category"] = {"$regex": category, "$options": "i"}
    if city:
        filter_query["city"] = {"$regex": city, "$options": "i"}

    total = await Business.find(filter_query).count()
    pages = math.ceil(total / size) if total > 0 else 0
    businesses = await Business.find(filter_query).skip((page - 1) * size).limit(size).sort("-created_at").to_list()

    return {"items": businesses, "total": total, "page": page, "size": size, "pages": pages}

@router.get("/business/{id}", response_model=BusinessResponse)
async def get_business(id: str, current_user: CurrentUser) -> Any:
    from beanie import PydanticObjectId
    business = await Business.get(PydanticObjectId(id))
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@router.post("/save", response_model=SavedLeadResponse)
async def save_lead(lead_in: SavedLeadCreate, current_user: CurrentUser) -> Any:
    from beanie import PydanticObjectId
    business = await Business.get(PydanticObjectId(lead_in.business_id))
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    existing = await SavedLead.find_one(
        SavedLead.user_id == str(current_user.id),
        SavedLead.business_id == lead_in.business_id,
        SavedLead.is_deleted == False
    )
    if existing:
        existing.status = lead_in.status
        if lead_in.tags:
            existing.tags = lead_in.tags
        if lead_in.notes is not None:
            existing.notes = lead_in.notes
        await existing.save()
        return existing

    lead = SavedLead(
        user_id=str(current_user.id),
        business_id=lead_in.business_id,
        status=lead_in.status,
        tags=lead_in.tags or [],
        notes=lead_in.notes
    )
    await lead.insert()
    return lead

@router.delete("/delete")
async def delete_leads(ids: List[str], current_user: CurrentUser) -> Any:
    for lead_id in ids:
        lead = await SavedLead.find_one(SavedLead.id == lead_id, SavedLead.user_id == str(current_user.id))
        if lead:
            lead.is_deleted = True
            await lead.save()
    return {"message": f"Successfully deleted {len(ids)} leads"}

@router.get("/saved", response_model=List[SavedLeadResponse])
async def get_saved_leads(current_user: CurrentUser) -> Any:
    leads = await SavedLead.find(
        SavedLead.user_id == str(current_user.id),
        SavedLead.is_deleted == False
    ).sort("-created_at").to_list()
    return leads

@router.post("/business/{id}/refresh")
async def refresh_business(id: str, current_user: CurrentUser) -> Any:
    business = await Business.find_one(Business.id == id, Business.is_deleted == False)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    from datetime import datetime
    business.last_checked = datetime.utcnow()
    await business.save()
    return {"status": "success", "message": "Business refreshed"}

@router.post("/export")
async def export_leads(current_user: CurrentUser) -> Any:
    return Response(content="id,business_name,email\n1,Test,test@test.com", media_type="text/csv")

from app.schemas.scout import DiscoverRequest, DiscoverResponse
from app.services.discovery.orchestrator import ScoutAgentOrchestrator

@router.post("/discover", response_model=DiscoverResponse)
async def discover_businesses(
    request: DiscoverRequest,
    current_user: CurrentUser
) -> Any:
    """
    Trigger the real-time Scout AI Agent.
    It automatically infers intent, searches, crawls, dedups and analyzes.
    """
    agent = ScoutAgentOrchestrator(str(current_user.id))
    result = await agent.execute_agent(raw_query=request.query)
    return result

from fastapi.responses import StreamingResponse

@router.get("/discover/stream")
async def stream_discover(query: str, current_user: CurrentUser) -> Any:
    """
    Stream the execution progress of the LangGraph multi-agent system using SSE.
    """
    from app.search.agent import build_scout_graph
    import json
    import asyncio
    
    graph = build_scout_graph()
    
    async def event_generator():
        state = {"user_id": str(current_user.id), "query": query, "status": "running", "progress": [], "errors": [], "search_queries": [], "raw_urls": [], "unique_urls": [], "crawled_data": [], "analyzed_businesses": [], "saved_business_ids": []}
        
        try:
            # Run LangGraph streaming
            async for output in graph.astream(state):
                # LangGraph yields a dict with node name as key and state delta as value
                node_name = list(output.keys())[0]
                node_state = output[node_name]
                
                # Check what progress items were added
                if "progress" in node_state:
                    # Stream the latest progress
                    for msg in node_state["progress"]:
                        yield f"data: {json.dumps({'status': 'progress', 'message': msg})}\n\n"
                        
            # After complete
            yield f"data: {json.dumps({'status': 'completed', 'message': 'Completed successfully'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")
