import asyncio
from app.services.risk_service import RiskService

async def main():
    ticker = "NVDA"
    print(f"\n--- Debugging Risk Analysis for {ticker} ---")
    
    # Initialize Service
    risk_service = RiskService()
    await risk_service.initialize()
    
    # Run Analysis
    print("\nRunning Analysis...")
    result = await risk_service.analyze(ticker, use_live_data=True)
    
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
