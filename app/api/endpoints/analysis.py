from fastapi import APIRouter, HTTPException
from app.schemas.risk import AnalysisRequest, AnalysisResponse
from app.services.risk_service import risk_service

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_company(request: AnalysisRequest):
    try:
        # Service returns a dictionary matching the response model
        result = await risk_service.analyze(request.ticker, request.use_live_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
