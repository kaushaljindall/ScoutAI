from fastapi import APIRouter, HTTPException
from typing import Any
from app.api.deps import CurrentUser
from app.schemas.ai import BusinessAnalysisResponse
from app.core.config import settings
from app.services.ai.provider import GeminiProvider
from app.models.scout import BusinessAnalysis, Business

router = APIRouter()

def get_ai_provider():
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Provider API key not configured")
    return GeminiProvider(api_key=settings.GEMINI_API_KEY)

@router.post("/analyze/{business_id}", response_model=BusinessAnalysisResponse)
async def analyze_business(business_id: str, current_user: CurrentUser) -> Any:
    from beanie import PydanticObjectId
    business = await Business.get(PydanticObjectId(business_id))
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    existing = await BusinessAnalysis.find_one(BusinessAnalysis.business_id == business_id)
    if existing:
        return existing

    try:
        provider = get_ai_provider()
        from app.services.ai.analyzer import AIService
        service = AIService(provider=provider)
        analysis_data = await service.analyze(business)
        analysis = BusinessAnalysis(business_id=business_id, **analysis_data)
        await analysis.insert()
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reanalyze/{business_id}", response_model=BusinessAnalysisResponse)
async def reanalyze_business(business_id: str, current_user: CurrentUser) -> Any:
    existing = await BusinessAnalysis.find_one(BusinessAnalysis.business_id == business_id)
    if existing:
        await existing.delete()
    return await analyze_business(business_id, current_user)

@router.get("/business/{business_id}", response_model=BusinessAnalysisResponse)
async def get_business_analysis(business_id: str, current_user: CurrentUser) -> Any:
    analysis = await BusinessAnalysis.find_one(BusinessAnalysis.business_id == business_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
