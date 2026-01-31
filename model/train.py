from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split

class RiskModel:
    def __init__(self, model_path: str = "data/gb_model.pkl"):
        self.model_path = model_path
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=4,
            random_state=42
        )
        self.features = ["debt_to_equity", "quick_ratio", "current_ratio", "return_on_equity", "free_cashflow", "volatility", "sentiment_risk_score"]

    def train(self, X: pd.DataFrame, y: pd.Series):
        """
        Train the Gradient Boosting Regressor.
        """
        X = X[self.features]
        print("Training model...")
        self.model.fit(X, y)
        print("Training complete.")
        self.save_model()

    def predict(self, X: pd.DataFrame) -> float:
        """
        Predict Probability of Default (PD).
        """
        # Ensure feature order
        X = X[self.features]
        # Predict continuous probability
        proba = self.model.predict(X)[0]
        # Clip to [0, 1] range just in case
        return float(max(0.0, min(1.0, proba)))

    def save_model(self):
        """Save model to pickle"""
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        """Load model from pickle"""
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
            print("Model loaded.")
        else:
            # Raise exception so main.py knows to train a new one
            raise FileNotFoundError("Model file not found.")

    def create_synthetic_data(self, n_samples=1000):
        """
        Generate synthetic training data with REALISTIC financial logic for demonstration.
        """
        np.random.seed(42)
        
        # 1. Healthy Companies (Majority)
        n_healthy = int(n_samples * 0.9)
        debt_to_equity_h = np.random.lognormal(mean=0, sigma=0.5, size=n_healthy) 
        quick_ratio_h = np.random.lognormal(mean=0, sigma=0.4, size=n_healthy)    
        current_ratio_h = quick_ratio_h + np.random.uniform(0, 0.5, n_healthy)
        return_on_equity_h = np.random.normal(0.1, 0.1, n_healthy)
        free_cashflow_h = np.random.normal(1e8, 5e7, n_healthy) # Positive Cashflow                
        volatility_h = np.random.lognormal(mean=0, sigma=0.2, size=n_healthy)     
        sentiment_score_h = np.random.beta(2, 5, n_healthy)                       

        # 2. Distressed Companies (Minority but critical)
        n_distressed = n_samples - n_healthy
        debt_to_equity_d = np.random.uniform(2.0, 10.0, size=n_distressed) # High Debt
        quick_ratio_d = np.random.uniform(0.1, 0.8, size=n_distressed)     # Liquidity Crisis
        current_ratio_d = quick_ratio_d + np.random.uniform(0, 0.2, n_distressed)
        return_on_equity_d = np.random.uniform(-0.5, -0.05, size=n_distressed) # Negative Returns
        free_cashflow_d = np.random.uniform(-1e9, -1e6, n_distressed)  # Burning Cash
        volatility_d = np.random.uniform(1.5, 4.0, size=n_distressed)      # High Volatility
        sentiment_score_d = np.random.beta(5, 2, n_distressed)             # Bad Sentiment

        # Combine
        debt_to_equity = np.concatenate([debt_to_equity_h, debt_to_equity_d])
        quick_ratio = np.concatenate([quick_ratio_h, quick_ratio_d])
        current_ratio = np.concatenate([current_ratio_h, current_ratio_d])
        return_on_equity = np.concatenate([return_on_equity_h, return_on_equity_d])
        free_cashflow = np.concatenate([free_cashflow_h, free_cashflow_d])
        volatility = np.concatenate([volatility_h, volatility_d])
        sentiment_score = np.concatenate([sentiment_score_h, sentiment_score_d])

        data = {
            "debt_to_equity": debt_to_equity,
            "quick_ratio": quick_ratio,
            "current_ratio": current_ratio,
            "return_on_equity": return_on_equity,
            "free_cashflow": free_cashflow,
            "volatility": volatility,
            "sentiment_risk_score": sentiment_score
        }
        df = pd.DataFrame(data)
        
        # Define Ground Truth Logic (Rule-based with heavy penalties)
        risk_score = (
            2.0 * (df["debt_to_equity"] > 2.5).astype(int) +
            2.0 * (df["quick_ratio"] < 0.6).astype(int) +
            3.0 * (df["return_on_equity"] < -0.05).astype(int) + # Heavy penalty for negative profits
            2.0 * (df["free_cashflow"] < 0).astype(int) +        # Burn Rate Penalty
            1.5 * (df["current_ratio"] < 0.8).astype(int) +
            1.0 * (df["volatility"] > 2.0).astype(int) +
            1.0 * (df["sentiment_risk_score"] > 0.6).astype(int) 
        )
        
        # Add slight noise
        risk_score += np.random.normal(0, 0.3, n_samples)
        
        # Sigmoid to probability
        # Shift so that "Safe" companies (score ~0-1) have very low PD
        # But "Distressed" companies (score > 5) have high PD
        probs = 1 / (1 + np.exp(-(risk_score - 7.5))) 
        
        return df, probs # Return continuous probabilities

if __name__ == "__main__":
    rm = RiskModel()
    X, y = rm.create_synthetic_data()
    rm.train(X, y)
    print(f"Sample prediction: {rm.predict(X.iloc[[0]])}")
