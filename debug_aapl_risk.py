import asyncio
from app.services.risk_service import RiskService

async def main():
    service = RiskService()
    await service.initialize()
    
    print("\n--- Analyzing AAPL ---")
    result = await service.analyze("AAPL", use_live_data=True)
    
    print("\n--- Analysis Result ---")
    print(f"Risk Level: {result['risk_level']}")
    print(f"PD: {result['probability_of_default']}")
    
    print("\n--- Financial Metrics ---")
    for k, v in result['financial_metrics'].items():
        print(f"{k}: {v}")
        
    print("\n--- Risk Factors (SHAP/Coefficients proxy) ---")
    for k, v in result['risk_factors'].items():
        print(f"{k}: {v}")
        
    print("\n--- RAG Evidences ---")
    for i, ev in enumerate(result['rag_evidences']):
        print(f"[{i+1}] {ev[:200]}...") # Print first 200 chars


if __name__ == "__main__":
    asyncio.run(main())
