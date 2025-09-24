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

logger = get_logger("weaviate_client")
try:
    import weaviate
    WEAVIATE_AVAILABLE = True
except Exception:
    weaviate = None
    WEAVIATE_AVAILABLE = False
    logger.warning("weaviate-client not installed; weaviate client disabled.")


class WeaviateClientWrapper:
    def __init__(self, url: str = None):
        self.url = url or settings.WEAVIATE_URL
        if WEAVIATE_AVAILABLE and self.url:
            self.client = weaviate.Client(self.url)
        else:
            self.client = None

    def upsert(self, items: List[dict]):
        if not self.client:
            logger.warning("weaviate client not configured; upsert is a no-op")
            return
        # production: implement batching and class schema checks
        for it in items:
            self.client.batch.add_data_object(it["metadata"], "Document", vector=it.get("vector"))
        self.client.batch.create_objects()
