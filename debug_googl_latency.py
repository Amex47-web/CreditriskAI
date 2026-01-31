import asyncio
from app.services.risk_service import RiskService
import time
import traceback

async def main():
    print("--- Initializing RiskService ---")
    start_init = time.time()
    service = RiskService()
    await service.initialize()
    print(f"Initialization took: {time.time() - start_init:.2f}s")
    
    ticker = "GOOGL"
    print(f"\n--- Analyzing {ticker} (Expect Auto-Download) ---")
    start_time = time.time()
    
    try:
        # Measure time for analysis
        result = await service.analyze(ticker, use_live_data=True)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"\nAnalysis Successful!")
        print(f"Total Duration: {duration:.2f}s")
        print(f"Risk Level: {result.get('risk_level')}")
        
        # Check evidences
        evidences = result.get('rag_evidences', [])
        print(f"Evidences found: {len(evidences)}")
        
    except Exception as e:
        print(f"\n[ERROR] Analysis Failed after {time.time() - start_time:.2f}s")
        print(str(e))
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
