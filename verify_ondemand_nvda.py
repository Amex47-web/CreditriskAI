import asyncio
from app.services.risk_service import RiskService
import os

async def main():
    service = RiskService()
    await service.initialize()
    
    ticker = "NVDA"
    print(f"\n--- Analyzing {ticker} (Expect Auto-Download) ---")
    
    data_dir = "data/filings"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Check if file exists BEFORE
    files_before = [f for f in os.listdir(data_dir) if "NVDA" in f]
    print(f"NVDA filings before: {len(files_before)}")
    
    # This might take a while due to download
    result = await service.analyze(ticker, use_live_data=True)
    
    # Check if file exists AFTER
    files_after = [f for f in os.listdir(data_dir) if "NVDA" in f]
    print(f"NVDA filings after: {len(files_after)}")
    
    if len(files_after) > len(files_before):
        print("[PASS] File was downloaded.")
    else:
        print("[FAIL] File was NOT downloaded.")

    print("\n--- RAG Evidences ---")
    for i, ev in enumerate(result['rag_evidences']):
        print(f"[{i+1}] {ev[:200]}...") 
        
    if any("NVDA" in ev or "NVIDIA" in ev.upper() for ev in result['rag_evidences']):
         print("[PASS] Found NVDA specific evidence.")
    else:
         print("[WARN] Did not find explicit NVDA mention, but might be due to chunking.")

if __name__ == "__main__":
    asyncio.run(main())
