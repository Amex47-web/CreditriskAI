from .embeddings import EmbeddingGenerator
from .vector_store import VectorStore
from typing import List
import numpy as np

class Retriever:
    def __init__(self, index_path: str = "data/faiss_index.bin"):
        print("Initializing Advanced Retriever...")
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore(index_file=index_path)
        self.vector_store.load()
        
        # Initialize Sparse Retriever (BM25)
        self.bm25 = None
        if self.vector_store.documents:
            self._build_bm25()
            
        # Initialize Cross-Encoder for Re-ranking (Lazy load)
        self.cross_encoder = None

    def _build_bm25(self):
        try:
            from rank_bm25 import BM25Okapi
            print("Building BM25 Index...")
            tokenized_corpus = [doc.lower().split() for doc in self.vector_store.documents]
            self.bm25 = BM25Okapi(tokenized_corpus)
        except ImportError:
            print("Warning: rank_bm25 not installed. Sparse retrieval disabled.")
        except Exception as e:
            print(f"Error building BM25: {e}")

    def _load_cross_encoder(self):
        if self.cross_encoder: return
        try:
            from sentence_transformers import CrossEncoder
            print("Loading Cross-Encoder for Re-ranking...")
            # 'cross-encoder/ms-marco-MiniLM-L-6-v2' is fast and effective
            self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2') 
        except Exception as e:
            print(f"Warning: Could not load Cross-Encoder ({e}). Re-ranking disabled.")

    def ingest_documents(self, documents: List[str], metadatas: List[dict] = None):
        """
        Embed and index a list of documents with optional metadata.
        """
        print("Generating embeddings for ingestion...")
        embeddings = self.embedder.generate(documents)
        self.vector_store.add_documents(embeddings, documents, metadatas)
        self.vector_store.save()
        # Rebuild BM25
        self._build_bm25()

    def retrieve(self, query: str, top_k: int = 5, filter: dict = None) -> List[str]:
        """
        Hybrid Retrieval + Re-ranking
        1. Dense Retrieval (FAISS)
        2. Sparse Retrieval (BM25)
        3. RRF Fusion (Optional) or Union
        4. Re-ranking (Cross-Encoder)
        """
        # 1. Dense Retrieval
        query_emb = self.embedder.generate([query])[0]
        # Pass filter to vector store
        dense_results = self.vector_store.search(query_emb, k=top_k, filter=filter) # List[(text, score)]
        
        # 2. Sparse Retrieval
        sparse_texts = []
        if self.bm25:
            tokenized_query = query.lower().split()
            # Get all scores
            doc_scores = self.bm25.get_scores(tokenized_query)
            
            # Filter scores
            if filter:
                # We need to zero out scores for docs that don't match filter
                # Iterate over all docs? Optimization: iterate over only non-zero scores if possible, 
                # but get_scores returns dense array.
                for idx, score in enumerate(doc_scores):
                    if score > 0:
                        doc_meta = self.vector_store.metadatas[idx] if idx < len(self.vector_store.metadatas) else {}
                        for key, val in filter.items():
                            if doc_meta.get(key) != val:
                                doc_scores[idx] = 0.0
                                break
            
            # Get top k indices
            top_n = np.argsort(doc_scores)[::-1][:top_k]
            sparse_texts = [self.vector_store.documents[i] for i in top_n if doc_scores[i] > 0]
        
        # 3. Combine Candidates (Union)
        # Use a dict to avoid duplicates
        candidates = {text: 0.0 for text, score in dense_results}
        for text in sparse_texts:
            if text not in candidates:
                candidates[text] = 0.0 # Score placeholder
                
        unique_candidates = list(candidates.keys())
        
        # 4. Re-Ranking (Cross-Encoder)
        self._load_cross_encoder()
        
        if self.cross_encoder and unique_candidates:
            pairs = [[query, doc] for doc in unique_candidates]
            scores = self.cross_encoder.predict(pairs)
            
            # Sort by score descending
            ranked_results = sorted(zip(unique_candidates, scores), key=lambda x: x[1], reverse=True)
            return [doc for doc, score in ranked_results[:top_k]]
            
        else:
            # Fallback if no cross-encoder: just return dense results first, then sparse
            # Or better, just return the dense ones if we have them, or whatever we have
            # Since dense usually has scores, let's prioritize dense.
             return [text for text, score in dense_results] if dense_results else sparse_texts[:top_k]

if __name__ == "__main__":
    retriever = Retriever()
    # Test logic
    # retriever.ingest_documents(["Apple is a tech company.", "Apples are delicious fruits."])
    # print(retriever.retrieve("financial report of Apple"))
