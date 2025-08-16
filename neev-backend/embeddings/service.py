"""
NEEV - Embedding Service
This service:
- Loads a multilingual sentence-transformer
- Encodes NCO entries into vectors
- Prepares vectors for FAISS index
"""

from typing import List, Dict, Tuple
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception as e:
    # Friendly message if sentence-transformers is not installed
    raise RuntimeError("Please install dependencies: pip install -r requirements.txt") from e

class EmbeddingService:
    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        self.nco_entries: List[Dict] = []
        self.embeddings: np.ndarray = None

    def load_nco(self, data: List[Dict]) -> None:
        """Store entries; later we’ll add validation/hierarchy checks."""
        self.nco_entries = data

    def _compose_text(self, item: Dict]) -> str:
        """
        What we encode: title + description.
        We can tweak fields later for better performance.
        """
        title = item.get("title_norm") or item.get("title") or ""
        desc = item.get("desc_norm") or item.get("description") or ""
        return f"{title} [SEP] {desc}"

    def encode(self) -> np.ndarray:
        if not self.nco_entries:
            raise ValueError("No NCO entries loaded")
        corpus = [self._compose_text(x) for x in self.nco_entries]
        self.embeddings = self.model.encode(corpus, convert_to_numpy=True, normalize_embeddings=True)
        return self.embeddings
