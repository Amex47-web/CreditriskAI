import pandas as pd
import numpy as np
from typing import Dict, List

class FeatureEngineer:
    def __init__(self):
        self.risk_keywords = ["default", "bankruptcy", "litigation", "investigation", "fraud", "material weakness", "restatement", "unsustainable", "going concern"]
        self.sentiment_analyzer = None

    def load_model(self):
        try:
            from nlp.sentiment import SentimentAnalyzer
            self.sentiment_analyzer = SentimentAnalyzer()
        except ImportError:
            print("Warning: nlp.sentiment module not found.")
        except Exception as e:
            print(f"Warning: Could not load FinBERT ({e}).")

    def compute_sentiment_score(self, text: str) -> float:
        """
        Compute risk score using FinBERT. 
        Returns probability of 'negative' sentiment [0.0, 1.0].
        """
        if self.sentiment_analyzer:
            return self.sentiment_analyzer.analyze(text)

        # Fallback: Simple keyword density normalized to [0,1] roughly
        text = text.lower()
        word_count = len(text.split())
        if word_count == 0: return 0.0
        match_count = sum(1 for word in self.risk_keywords if word in text)
        return min(match_count / 10.0, 1.0) # Cap at 1.0 for high keyword density

    def combine_features(self, financial_data: Dict[str, float], text_data: str) -> pd.DataFrame:
        """
        Combine quantitative financial metrics with qualitative text signals.
        """
        risk_score = self.compute_sentiment_score(text_data)
        
        features = {
            "debt_to_equity": financial_data.get("debt_to_equity", 0),
            "quick_ratio": financial_data.get("quick_ratio", 0),
            "current_ratio": financial_data.get("current_ratio", 0),
            "return_on_equity": financial_data.get("return_on_equity", 0),
            "free_cashflow": financial_data.get("free_cashflow", 0), # New Feature
            "volatility": financial_data.get("beta", 0), 
            "sentiment_risk_score": risk_score
        }
        
        # Handle None values with Risk-Aware Imputation
        defaults = {
            "debt_to_equity": 5.0,      # Assume high debt if missing
            "quick_ratio": 0.5,         # Assume low liquidity
            "current_ratio": 0.5,       # Assume low liquidity
            "return_on_equity": -0.1,   # Assume negative return
            "free_cashflow": -1e6,      # Assume negative cashflow if missing
            "volatility": 2.0,          # Assume high volatility
            "sentiment_risk_score": 0.5 # Neutral-High risk
        }

        for k, v in features.items():
            if v is None:
                features[k] = defaults.get(k, 0.0)
                
        return pd.DataFrame([features])

if __name__ == "__main__":
    fe = FeatureEngineer()
    fin_data = {"debt_to_equity": 1.5, "quick_ratio": 0.8}
    text = "The company faces significant litigation and potential bankruptcy risks."
    df = fe.combine_features(fin_data, text)
    print(df)
