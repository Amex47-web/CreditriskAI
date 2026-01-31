import pandas as pd
from typing import Dict, Any
import asyncio
from data.finance_loader import FinanceLoader
from nlp.retriever import Retriever
from model.features import FeatureEngineer
from model.train import RiskModel
from model.explainers import Explainer
from data.sec_loader import SECLoader
from data.ingest import ingest_filings

class RiskService:
    def __init__(self):
        self.finance_loader = FinanceLoader()
        self.retriever = None
        self.risk_model = RiskModel()
        self.feature_engineer = FeatureEngineer()
        self.explainer = None
        self.initialized = False

    async def initialize(self):
        if self.initialized:
            return
        
        print("Initializing Risk Service Components...")
        
        # Initialize Retriever (loads FAISS)
        try:
            self.retriever = Retriever()
        except Exception as e:
            print(f"Warning: Could not load Retriever ({e}). RAG features may be limited.")
        
        # Load Risk Model
        try:
            self.risk_model.load_model()
        except:
            print("Warning: Model not found. Creating synthetic model for demo.")
            X, y = self.risk_model.create_synthetic_data()
            self.risk_model.train(X, y)
            
        # Initialize Explainer
        try:
            self.explainer = Explainer(self.risk_model)
        except Exception as e:
            print(f"Warning: Could not initialize Explainer ({e}).")
            
        # Initialize Feature Engineer (loads FinBERT)
        self.feature_engineer.load_model()
            
        self.initialized = True

    async def analyze(self, ticker: str, use_live_data: bool = True) -> Dict[str, Any]:
        ticker = ticker.upper()
        
        # 1. Fetch Financial Data
        try:
            if use_live_data:
                fin_data = self.finance_loader.get_fundamental_data(ticker)
            else:
                # Dummy data for default/offline testing
                fin_data = {
                    "ticker": ticker,
                    "debt_to_equity": 1.2,
                    "quick_ratio": 0.9,
                    "current_ratio": 1.1,
                    "return_on_equity": 0.15,
                    "beta": 1.1
                }
        except Exception as e:
            raise Exception(f"Error fetching financial data: {str(e)}")

        # 2. Retrieve Text Evidences (RAG)
        try:
            # Query for general risk
            query = f"Risk factors and default warnings for {ticker}"
            # Filter by ticker to ensure we don't get references for other companies
            filter_criteria = {"ticker": ticker}
            evidences = self.retriever.retrieve(query, top_k=3, filter=filter_criteria) if self.retriever else []
            
            # Check if we have valid evidences, if not attempt to download
            if not evidences and self.retriever and use_live_data:
                print(f"No documents found for {ticker}. Attempting on-demand retrieval...")
                try:
                    loader = SECLoader()
                    downloaded_files = loader.fetch_company_filings(ticker, count=1)
                    if downloaded_files:
                        # Run ingestion in a separate thread to avoid blocking the event loop
                        await asyncio.to_thread(ingest_filings, specific_files=downloaded_files, retriever_instance=self.retriever)
                        # Retry retrieval
                        evidences = self.retriever.retrieve(query, top_k=3, filter=filter_criteria)
                except Exception as e:
                    print(f"On-demand retrieval failed: {e}")

            # If no evidences found (empty vector store or download failed), use placeholder
            if not evidences:
                evidences = [f"No specific documents found for {ticker}. Using general market risk assessment."]
                
            combined_text = " ".join(evidences)
        except Exception as e:
            print(f"RAG Error: {e}")
            evidences = []
            combined_text = ""

        # 3. Feature Engineering
        features_df = self.feature_engineer.combine_features(fin_data, combined_text)
        
        # 4. Predict Risk
        pd_prob = self.risk_model.predict(features_df)
        
        # 5. Explainability
        shap_values = {}
        if self.explainer:
            shap_values = self.explainer.explain_prediction(features_df)
            # Convert float32 to float for JSON serialization
            shap_values = {k: float(v) for k, v in shap_values.items()}

        # 6. Construct Response
        response = {
            "ticker": ticker,
            "probability_of_default": float(pd_prob),
            "risk_level": "High" if pd_prob > 0.10 else "Low",
            "financial_metrics": fin_data,
            "rag_evidences": evidences,
            "risk_factors": shap_values
        }
        
        return response

# Singleton instance
risk_service = RiskService()
