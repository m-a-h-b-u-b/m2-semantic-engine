# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

from typing import List, Callable, Dict
from ..retrieval.retriever import Retriever
from ..utils.logger import get_logger

logger = get_logger("rag")

class RAGPipeline:
    def __init__(self, retriever: Retriever = None, llm_fn: Callable[[str], str] = None):
        self.retriever = retriever or Retriever()
        # llm_fn is a callable that takes prompt:str and returns completions:str
        self.llm_fn = llm_fn or (lambda prompt: "LLM not configured. Please provide llm_fn.")

    def answer(self, query: str, top_k: int = 5) -> Dict:
        # 1. retrieve
        hits = self.retriever.retrieve(query, top_k=top_k)
        # 2. build context
        context = "\n\n".join([f"### doc {h['id']}\n{h['text']}" for h in hits])
        prompt = f"Use the following retrieved documents to answer the question.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        logger.info("prompt length: %d", len(prompt))
        # 3. call llm
        response = self.llm_fn(prompt)
        return {"answer": response, "retrieved": hits}
