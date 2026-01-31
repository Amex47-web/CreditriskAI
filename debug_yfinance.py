import yfinance as yf

ticker = "AAPL"
stock = yf.Ticker(ticker)
info = stock.info

print(f"Ticker: {ticker}")
print(f"DebtToEquity (Raw from yfinance): {info.get('debtToEquity')}")
print(f"ReturnOnEquity (Raw from yfinance): {info.get('returnOnEquity')}")
print(f"QuickRatio: {info.get('quickRatio')}")
print(f"CurrentRatio: {info.get('currentRatio')}")
print(f"Beta: {info.get('beta')}")
