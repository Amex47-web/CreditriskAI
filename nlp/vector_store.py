import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple

class VectorStore:
    def __init__(self, dimension: int = 384, index_file: str = "faiss_index.bin"):
        """
        Initialize FAISS index.
        :param dimension: Dimension of embeddings (384 for MiniLM-L6-v2).
        """
        self.dimension = dimension
        self.index_file = index_file
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []  # Store text mapping
        self.metadatas = []  # Store metadata (e.g. {"ticker": "AAPL"})

    def add_documents(self, embeddings: np.ndarray, texts: List[str], metadatas: List[dict] = None):
        """
        Add documents to the index.
        """
        if len(texts) != embeddings.shape[0]:
            raise ValueError("Number of texts and embeddings must match.")
        
        if metadatas and len(metadatas) != len(texts):
            raise ValueError("Number of metadatas must match number of texts.")
            
        self.index.add(embeddings)
        self.documents.extend(texts)
        if metadatas:
            self.metadatas.extend(metadatas)
        else:
            # Add empty dicts if no metadata provided to keep indices aligned
            self.metadatas.extend([{} for _ in texts])
            
        print(f"Added {len(texts)} documents to vector store.")

    def search(self, query_embedding: np.ndarray, k: int = 5, filter: dict = None) -> List[Tuple[str, float]]:
        """
        Search for similar documents with optional filtering.
        """
        # Faiss expects 2D array
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
            
        # If we have a filter, we might need to fetch more candidates to ensure we have enough after filtering
        search_k = k * 10 if filter else k
        
        distances, indices = self.index.search(query_embedding, search_k)
        
        results = []
        found_count = 0
        
        for i in range(search_k):
            # Safe check for index bounds (FAISS can return -1)
            if i >= len(indices[0]): break
            
            idx = indices[0][i]
            if idx != -1 and idx < len(self.documents):
                # Check filter
                if filter:
                    match = True
                    # Metadata for this doc
                    doc_meta = self.metadatas[idx] if idx < len(self.metadatas) else {}
                    
                    for key, val in filter.items():
                        if doc_meta.get(key) != val:
                            match = False
                            break
                    if not match:
                        continue
                
                results.append((self.documents[idx], float(distances[0][i])))
                found_count += 1
                if found_count >= k:
                    break
        
        return results

    def save(self):
        """
        Save index and documents/metadata to disk.
        """
        faiss.write_index(self.index, self.index_file)
        with open(self.index_file + ".pkl", "wb") as f:
            data = {
                "documents": self.documents,
                "metadatas": self.metadatas
            }
            pickle.dump(data, f)
        print(f"Index saved to {self.index_file}")

    def load(self):
        """
        Load index and documents from disk.
        """
        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
            if os.path.exists(self.index_file + ".pkl"):
                with open(self.index_file + ".pkl", "rb") as f:
                    data = pickle.load(f)
                    # Handle legacy format where data was just a list of strings
                    if isinstance(data, list):
                        self.documents = data
                        self.metadatas = [{} for _ in data]
                    elif isinstance(data, dict):
                        self.documents = data.get("documents", [])
                        self.metadatas = data.get("metadatas", [])
            print(f"Index loaded from {self.index_file}")
        else:
            print("Index file not found, starting fresh.")

if __name__ == "__main__":
    # Test
    vs = VectorStore(384)
    # simulate embeddings
    dummy_emb = np.random.random((2, 384)).astype('float32')
    vs.add_documents(dummy_emb, ["doc1", "doc2"])
    res = vs.search(dummy_emb[0])
    print(res)
