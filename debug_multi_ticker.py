import asyncio
import pandas as pd
from app.services.risk_service import RiskService

async def main():
    service = RiskService()
    await service.initialize()
    
    tickers = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"]
    results = []
    
    print(f"\n{'Ticker':<10} | {'PD':<15} | {'Risk Level':<10} | {'Beta':<10} | {'Sentiment':<10}")
    print("-" * 70)
    
    for t in tickers:
        res = await service.analyze(t, use_live_data=True)
        pd_val = res['probability_of_default']
        beta = res['financial_metrics'].get('beta', 0)
        risk_score = res['risk_factors'].get('sentiment_risk_score', 0) # This is actually SHAP, specifically we want input sentiment
        
        # Extract input sentiment from feature engineer if possible, but for now looking at output
        # Let's just print the PD (probability)
        print(f"{t:<10} | {pd_val:<15.10f} | {res['risk_level']:<10} | {beta:<10.2f} | {res['risk_factors'].get('volatility', 'N/A')}")
        results.append(res)

if __name__ == "__main__":
    asyncio.run(main())
