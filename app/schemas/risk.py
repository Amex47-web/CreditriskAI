from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class AnalysisRequest(BaseModel):
    ticker: str
    use_live_data: bool = True

class AnalysisResponse(BaseModel):
    ticker: str
    probability_of_default: float
    risk_level: str
    financial_metrics: Dict[str, Any]
    rag_evidences: List[str]
    risk_factors: Dict[str, float]
