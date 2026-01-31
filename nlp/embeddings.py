from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)

    def generate(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for a list of texts or a single string.
        """
        embeddings = self.model.encode(texts)
        return embeddings

if __name__ == "__main__":
    generator = EmbeddingGenerator()
    emb = generator.generate(["This is a test document.", "Another financial report."])
    print(f"Embedding shape: {emb.shape}")
