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
    business = await Business.find_one(Business.id == id, Business.is_deleted == False)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@router.post("/save", response_model=SavedLeadResponse)
async def save_lead(lead_in: SavedLeadCreate, current_user: CurrentUser) -> Any:
    business = await Business.find_one(Business.id == lead_in.business_id)
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

@router.get("/leads", response_model=List[SavedLeadResponse])
async def get_leads(current_user: CurrentUser) -> Any:
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
