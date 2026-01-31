import yfinance as yf
import pandas as pd
import numpy as np

ticker = "BYND"
stock = yf.Ticker(ticker)
info = stock.info

print(f"--- Data for {ticker} ---")
print(f"DebtToEquity: {info.get('debtToEquity')}")
print(f"QuickRatio: {info.get('quickRatio')}")
print(f"CurrentRatio: {info.get('currentRatio')}")
print(f"ReturnOnEquity: {info.get('returnOnEquity')}")
print(f"FreeCashflow: {info.get('freeCashflow')}")

# Check type of missing values
roe = info.get('returnOnEquity')
print(f"ROE Type: {type(roe)}")
