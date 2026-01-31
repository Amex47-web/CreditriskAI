import yfinance as yf
import pandas as pd
from typing import Dict, Any

class FinanceLoader:
    def __init__(self):
        pass

    def get_fundamental_data(self, ticker: str) -> Dict[str, Any]:
        """
        Get key fundamental ratios and metrics for risk analysis.
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract key risk indicators
        debt_to_equity = info.get("debtToEquity")
        if debt_to_equity is not None:
            debt_to_equity = debt_to_equity / 100

        data = {
            "ticker": ticker,
            "current_price": info.get("currentPrice"),
            "debt_to_equity": debt_to_equity,
            "quick_ratio": info.get("quickRatio"),
            "current_ratio": info.get("currentRatio"),
            "return_on_equity": info.get("returnOnEquity"),
            "free_cashflow": info.get("freeCashflow"),
            "market_cap": info.get("marketCap"),
            "sector": info.get("sector"),
            "beta": info.get("beta")
        }
        return data

    def get_market_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Get historical market data for volatility calculation.
        """
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist

    def calculate_volatility(self, hist_data: pd.DataFrame, window: int = 30) -> float:
        """
        Calculate annualized volatility based on daily returns.
        """
        if hist_data.empty:
            return 0.0
        
        hist_data['Returns'] = hist_data['Close'].pct_change()
        volatility = hist_data['Returns'].rolling(window=window).std().iloc[-1]
        
        # Annualize (assuming 252 trading days)
        annualized_vol = volatility * (252 ** 0.5)
        return annualized_vol

if __name__ == "__main__":
    loader = FinanceLoader()
    print(loader.get_fundamental_data("AAPL"))
