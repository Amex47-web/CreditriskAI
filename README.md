# Credit Risk & Default Prediction System (Open Source)

A fully free, open-source Credit Risk system leveraging NLP and Retrieval-Augmented Generation (RAG) to analyze financial data and annual reports.

## Features
- **Data Ingestion**: Automates downloads of SEC filings and stock data.
- **RAG Engine**: Retrieves evidence from 10-K/10-Q reports.
- **Risk Scoring**: Uses XGBoost + Financial Ratios + Sentiment Analysis.
- **Explainability**: SHAP values and text citations for transparency.

## Tech Stack
- **Python**: Core logic
- **FastAPI**: Backend API
- **FAISS**: Vector Search
- **XGBoost**: Classification Model
- **SentenceTransformers**: Embeddings

## Setup
1. `pip install -r requirements.txt`
2. Run data loaders (see `data/` folder).
3. Start API: `run_api.sh`
