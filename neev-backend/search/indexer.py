"""
NEEV - FAISS Indexer
- Builds a Flat (exact) FAISS index for ~3,600 vectors (fast enough on CPU)
- Provides top-k search
"""

from typing import List, Dict, Tuple
import numpy as np
import faiss

class FaissIndexer:
    def __init__(self):
        self.index = None
        self.id_to_meta: List[Dict] = []

    def build(self, embeddings: np.ndarray, metadata: List[Dict]) -> None:
        """
        Build a cosine-similarity-like index by using normalized vectors and inner product.
        """
        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be 2D array of shape (N, D)")
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # Inner Product on normalized vectors ~= cosine
        self.index.add(embeddings)
        self.id_to_meta = metadata

    def search(self, query_vec: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        """
        query_vec: shape (D,) or (1, D) normalized
        Returns: list of (metadata, score)
        """
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1)
        scores, ids = self.index.search(query_vec, k)
        results = []
        for i, sc in zip(ids, scores):
            if i == -1:
                continue
            results.append((self.id_to_meta[i], float(sc)))
        return results
