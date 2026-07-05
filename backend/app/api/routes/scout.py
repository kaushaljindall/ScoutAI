import math
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Response
from sqlalchemy import or_
from app.api.deps import SessionDep, CurrentUser
from app.models.scout import Business, SavedLead
from app.schemas.scout import BusinessResponse, PaginatedBusinesses, SavedLeadCreate, SavedLeadResponse

router = APIRouter()

@router.get("/search", response_model=PaginatedBusinesses)
def search_businesses(
    db: SessionDep,
    current_user: CurrentUser,
    q: Optional[str] = None,
    category: Optional[str] = None,
    city: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
) -> Any:
    """
    Search businesses in the database
    """
    query = db.query(Business).filter(Business.is_deleted == False)

    if q:
        search_filter = or_(
            Business.business_name.ilike(f"%{q}%"),
            Business.website.ilike(f"%{q}%"),
            Business.email.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)

    if category:
        query = query.filter(Business.category.ilike(f"%{category}%"))
        
    if city:
        query = query.filter(Business.city.ilike(f"%{city}%"))

    total = query.count()
    pages = math.ceil(total / size) if total > 0 else 0
    
    businesses = query.order_by(Business.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return {
        "items": businesses,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

@router.get("/business/{id}", response_model=BusinessResponse)
def get_business(
    id: str,
    db: SessionDep,
    current_user: CurrentUser
) -> Any:
    """
    Get business details by ID
    """
    business = db.query(Business).filter(Business.id == id, Business.is_deleted == False).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@router.post("/save", response_model=SavedLeadResponse)
def save_lead(
    lead_in: SavedLeadCreate,
    db: SessionDep,
    current_user: CurrentUser
) -> Any:
    """
    Save a business as a lead
    """
    business = db.query(Business).filter(Business.id == lead_in.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    existing_lead = db.query(SavedLead).filter(
        SavedLead.user_id == current_user.id,
        SavedLead.business_id == lead_in.business_id,
        SavedLead.is_deleted == False
    ).first()
    
    if existing_lead:
        # Update existing
        existing_lead.status = lead_in.status
        if lead_in.tags:
            existing_lead.tags = lead_in.tags
        if lead_in.notes is not None:
            existing_lead.notes = lead_in.notes
        db.commit()
        db.refresh(existing_lead)
        return existing_lead

    # Create new
    lead = SavedLead(
        user_id=current_user.id,
        business_id=lead_in.business_id,
        status=lead_in.status,
        tags=lead_in.tags,
        notes=lead_in.notes
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.delete("/delete")
def delete_leads(
    ids: List[str],
    db: SessionDep,
    current_user: CurrentUser
) -> Any:
    """
    Bulk delete saved leads
    """
    db.query(SavedLead).filter(
        SavedLead.id.in_(ids),
        SavedLead.user_id == current_user.id
    ).update({"is_deleted": True}, synchronize_session=False)
    db.commit()
    return {"message": f"Successfully deleted {len(ids)} leads"}

@router.post("/export")
def export_leads(
    db: SessionDep,
    current_user: CurrentUser
) -> Any:
    """
    Export saved leads as CSV (Mock)
    """
    # In a real scenario, this would generate and return a CSV file
    return Response(content="id,business_name,email\n1,Test,test@test.com", media_type="text/csv")
