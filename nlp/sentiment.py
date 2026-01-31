from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import List, Dict

class SentimentAnalyzer:
    def __init__(self, model_name: str = "ProsusAI/finbert"):
        print(f"Loading Sentiment Model: {model_name}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            # using return_all_scores=True to get probas for all classes
            self.pipe = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer, return_all_scores=True)
            self.max_len = 512
        except Exception as e:
            print(f"Error loading FinBERT: {e}")
            self.pipe = None

    def analyze(self, text: str) -> float:
        """
        Analyzes the sentiment of the text using FinBERT.
        Handles long text by chunking.
        Returns a 'risk score' based on negative sentiment probability.
        """
        if not text or not self.pipe:
            return 0.0

        # Simple chunking by sliding window of tokens would be best, 
        # but for simplicity/speed we'll chunk by characters approx or split lines.
        # Let's do a reliable token-based chunking.
        
        inputs = self.tokenizer(text, return_tensors="pt", truncation=False, padding=False)
        input_ids = inputs['input_ids'][0]
        
        # If short enough, just run
        if len(input_ids) <= self.max_len:
            return self._predict_risk(text)
            
        # Sliding window
        stride = 256
        window = 510 # leave room for special tokens
        
        chunks = []
        for i in range(0, len(input_ids), stride):
            chunk_ids = input_ids[i : i + window]
            if len(chunk_ids) < 10: break # skip tiny chunks
            chunks.append(self.tokenizer.decode(chunk_ids, skip_special_tokens=True))
            
        if not chunks:
            return 0.0
            
        # Get scores for each chunk
        scores = []
        for chunk in chunks:
            scores.append(self._predict_risk(chunk))
            
        # Aggregate: Use mean to smooth out outlier negative chunks from standard disclosures.
        return float(np.mean(scores))

    def _predict_risk(self, text: str) -> float:
        try:
            # pipe output format: [[{'label': 'positive', 'score': 0.1}, ...]]
            results = self.pipe(text[:2000]) # backup truncation just in case, though we chunked
            flat_results = results[0] # List of dicts
            
            # Extract score for 'negative' label
            neg_score = next((r['score'] for r in flat_results if r['label'] == 'negative'), 0.0)
            neu_score = next((r['score'] for r in flat_results if r['label'] == 'neutral'), 0.0)
            
            # Risk = Negative Score + (0.1 * Neutral Score)
            return neg_score + (0.1 * neu_score)
        except Exception as e:
            print(f"Prediction error: {e}")
            return 0.0
