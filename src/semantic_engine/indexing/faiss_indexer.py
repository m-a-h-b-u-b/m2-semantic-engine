# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

from typing import List, Tuple
from ..utils.logger import get_logger
from ..settings import settings

logger = get_logger("faiss_indexer")
try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    faiss = None
    FAISS_AVAILABLE = False
    logger.warning("faiss not installed; faiss indexer will use an in-memory fallback.")

import numpy as np


class FaissIndexer:
    def __init__(self, dim: int = None):
        self.dim = dim or settings.EMBEDDING_DIM
        self.index = None
        self.docs = []  # map idx -> (id, metadata, text)
        self._init_index()

    def _init_index(self):
        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatL2(self.dim)
        else:
            self.index = None  # fallback to brute-force numpy

    def add(self, embeddings: List[List[float]], docs: List[dict]):
        n = len(embeddings)
        vecs = np.array(embeddings).astype("float32")
        if FAISS_AVAILABLE:
            self.index.add(vecs)
        else:
            # store vectors in RAM for fallback
            if not hasattr(self, "_vecs"):
                self._vecs = vecs
            else:
                self._vecs = np.vstack([self._vecs, vecs])
        base_idx = len(self.docs)
        for i, d in enumerate(docs):
            self.docs.append(d)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[dict, float]]:
        q = np.array([query_embedding]).astype("float32")
        if FAISS_AVAILABLE:
            distances, indices = self.index.search(q, top_k)
            out = []
            for idx, dist in zip(indices[0], distances[0]):
                if idx < len(self.docs):
                    out.append((self.docs[idx], float(dist)))
            return out
        else:
            # brute force
            vecs = getattr(self, "_vecs", None)
            if vecs is None:
                return []
            dists = np.linalg.norm(vecs - q, axis=1)
            order = np.argsort(dists)[:top_k]
            return [(self.docs[i], float(dists[i])) for i in order]
