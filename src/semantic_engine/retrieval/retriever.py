# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine


from typing import List, Dict
from ..embeddings.generator import EmbeddingGenerator
from ..indexing.faiss_indexer import FaissIndexer
from ..utils.logger import get_logger

logger = get_logger("retriever")


class Retriever:
    def __init__(self, embedding_model: str = None):
        self.embedder = EmbeddingGenerator(model_name=embedding_model)
        self.indexer = FaissIndexer(dim=self.embedder.dim)

    def index_documents(self, docs: List[Dict]):
        """
        docs: list of dicts, each with keys: id, text, metadata(optional)
        """
        texts = [d["text"] for d in docs]
        embeddings = self.embedder.embed(texts)
        # attach vectors for retrieval
        docs_with_meta = [{"id": d.get("id"), "text": d["text"], "metadata": d.get("metadata")} for d in docs]
        self.indexer.add(embeddings, docs_with_meta)

    def retrieve(self, query: str, top_k: int = 5):
        q_emb = self.embedder.embed([query])[0]
        results = self.indexer.search(q_emb, top_k=top_k)
        # results: list of (doc_dict, distance)
        return [{"id": doc["id"], "text": doc["text"], "metadata": doc.get("metadata"), "score": score} for doc, score in results]
