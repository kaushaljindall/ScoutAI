from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any
from uuid import UUID

from app.schemas.validation import ValidationRequest, ValidationStatusResponse, BusinessValidationResponse
from app.models.validation import ValidatedBusiness

router = APIRouter(prefix="/validation", tags=["validation"])

@router.post("/run", response_model=Dict[str, Any])
async def run_validation(request: ValidationRequest, background_tasks: BackgroundTasks):
    """Start the validation pipeline for a batch of businesses."""
    return {"message": "Validation pipeline started", "count": len(request.businesses)}

@router.get("/status/{business_id}", response_model=ValidationStatusResponse)
async def get_validation_status(business_id: UUID):
    """Get the current validation status of a business."""
    business = await ValidatedBusiness.get(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    return ValidationStatusResponse(
        id=business.id,
        business_name=business.business_name,
        status=business.status
    )

@router.post("/business/{business_id}", response_model=Dict[str, Any])
async def revalidate_business(business_id: UUID, background_tasks: BackgroundTasks):
    """Trigger re-validation for a specific business."""
    business = await ValidatedBusiness.get(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    return {"message": "Revalidation triggered", "business_id": str(business_id)}
