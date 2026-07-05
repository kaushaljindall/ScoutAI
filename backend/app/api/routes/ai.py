from fastapi import APIRouter, HTTPException, Depends
from typing import Any
from app.api.deps import SessionDep, CurrentUser
from app.schemas.ai import BusinessAnalysisResponse
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.services.ai.analyzer import AIService
from app.models.scout import BusinessAnalysis

router = APIRouter()

def get_ai_service(db: SessionDep) -> AIService:
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    provider = GeminiProvider(api_key=settings.GEMINI_API_KEY)
    return AIService(provider=provider, db=db)

@router.post("/analyze/{business_id}", response_model=BusinessAnalysisResponse)
def analyze_business(
    business_id: str,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Analyze a business using AI.
    """
    ai_service = get_ai_service(db)
    try:
        analysis = ai_service.analyze_business(business_id=business_id, force_reanalyze=False)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reanalyze/{business_id}", response_model=BusinessAnalysisResponse)
def reanalyze_business(
    business_id: str,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Force re-analyze a business.
    """
    ai_service = get_ai_service(db)
    try:
        analysis = ai_service.analyze_business(business_id=business_id, force_reanalyze=True)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/{business_id}", response_model=BusinessAnalysisResponse)
def get_business_analysis(
    business_id: str,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Get existing analysis for a business.
    """
    analysis = db.query(BusinessAnalysis).filter(BusinessAnalysis.business_id == business_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
