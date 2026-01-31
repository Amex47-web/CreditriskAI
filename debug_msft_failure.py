import asyncio
from app.services.risk_service import RiskService
import traceback

async def main():
    print("Initializing RiskService...")
    service = RiskService()
    await service.initialize()
    
    print("\n--- Analyzing MSFT ---")
    try:
        # Simulate real request with live data (triggers download)
        result = await service.analyze("MSFT", use_live_data=True)
        print("Analysis Successful!")
        print(f"Risk Level: {result.get('risk_level')}")
    except Exception as e:
        print("\n[ERROR] Analysis Failed!")
        print(str(e))
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
