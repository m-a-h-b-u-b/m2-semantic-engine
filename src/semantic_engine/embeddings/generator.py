# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

from typing import List
from ..utils.logger import get_logger
from ..settings import settings

logger = get_logger("embeddings")

# Try to import sentence_transformers; if not installed, fall back to a dummy generator
try:
    from sentence_transformers import SentenceTransformer
    MODEL_AVAILABLE = True
except Exception:
    SentenceTransformer = None
    MODEL_AVAILABLE = False
    logger.warning("sentence-transformers not installed; using dummy embeddings (random vectors).")

import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.dim = settings.EMBEDDING_DIM
        if MODEL_AVAILABLE:
            logger.info("loading embedding model: %s", self.model_name)
            self.model = SentenceTransformer(self.model_name)
            # override dim if model gives one:
            try:
                self.dim = self.model.get_sentence_embedding_dimension()
            except Exception:
                pass
        else:
            self.model = None

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self.model:
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            return embeddings.tolist()
        # deterministic-ish fallback: hash-based pseudo-embeddings
        embs = []
        for t in texts:
            h = abs(hash(t))
            rng = np.random.RandomState((h % (2**32 - 1)))
            embs.append(rng.normal(size=(self.dim,)).tolist())
        return embs
