# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..main import get_pipeline
from ...utils.metrics import queries_total, query_latency_seconds
import time

router = APIRouter()

class QueryIn(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryOut(BaseModel):
    answer: str
    retrieved: list

@router.post("/query", response_model=QueryOut)
async def query(q: QueryIn):
    start = time.time()
    queries_total.inc()
    pipeline = get_pipeline()
    try:
        with query_latency_seconds.time():
            res = pipeline.answer(q.query, top_k=q.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        elapsed = time.time() - start
    return res
