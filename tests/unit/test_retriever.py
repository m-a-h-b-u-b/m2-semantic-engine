# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

import pytest
from src.semantic_engine.retrieval.retriever import Retriever

def test_index_and_retrieve():
    r = Retriever()
    docs = [
        {"id": "d1", "text": "The capital of France is Paris."},
        {"id": "d2", "text": "Python is a programming language."},
        {"id": "d3", "text": "The Eiffel Tower is in Paris."},
    ]
    r.index_documents(docs)
    res = r.retrieve("What is the capital of France?", top_k=2)
    assert len(res) >= 1
    assert any("France" in r["text"] or "Paris" in r["text"] for r in res)
