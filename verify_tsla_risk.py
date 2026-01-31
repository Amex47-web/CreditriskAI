import asyncio
from app.services.risk_service import RiskService

async def main():
    service = RiskService()
    await service.initialize()
    
    print("\n--- Analyzing TSLA (Expect NO Apple docs) ---")
    result = await service.analyze("TSLA", use_live_data=True)
    
    print("\n--- RAG Evidences ---")
    found_apple = False
    for i, ev in enumerate(result['rag_evidences']):
        print(f"[{i+1}] {ev[:200]}...") 
        if "AAPL" in ev or "Apple" in ev:
            found_apple = True
            
    if found_apple:
        print("\n[FAIL] Found Apple references in TSLA analysis.")
    else:
        print("\n[PASS] No Apple references found for TSLA.")
        # Check if we got the fallback message
        if any("No specific documents found" in ev for ev in result['rag_evidences']):
            print("[INFO] Correctly fell back to generic assessment (since TSLA docs not ingested).")

if __name__ == "__main__":
    asyncio.run(main())
