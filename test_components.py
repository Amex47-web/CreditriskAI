import sys
import os
import traceback

# Add project root to path
sys.path.append(os.getcwd())

from data.finance_loader import FinanceLoader
from model.features import FeatureEngineer
from model.train import RiskModel
from model.explainers import Explainer
from nlp.retriever import Retriever

def debug():
    print("--- Starting Debug Session ---")
    
    # 1. Test Feature Engineer
    try:
        print("Initializing FeatureEngineer...")
        fe = FeatureEngineer()
        print("FeatureEngineer OK.")
    except Exception:
        traceback.print_exc()

    # 2. Test Risk Model (Synthetic)
    try:
        print("Initializing RiskModel...")
        rm = RiskModel()
        print("Training synthetic model...")
        X, y = rm.create_synthetic_data(100)
        rm.train(X, y)
        print("RiskModel trained OK.")
        
        print("Predicting...")
        sample = X.iloc[[0]]
        prob = rm.predict(sample)
        print(f"Prediction: {prob}")
    except Exception:
        traceback.print_exc()

    # 3. Test Explainer
    try:
        print("Initializing Explainer...")
        exp = Explainer(rm)
        print("Explainer OK.")
        
        print("Explaining prediction...")
        shap_vals = exp.explain_prediction(sample)
        print(f"SHAP Values: {shap_vals}")
    except Exception:
        traceback.print_exc()
        
    # 4. Test Retriever
    try:
        print("Initializing Retriever...")
        ret = Retriever() # might fail if no index
        print("Retriever OK.")
        print("Retrieving...")
        docs = ret.retrieve("risk")
        print(f"Docs found: {len(docs)}")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    debug()
