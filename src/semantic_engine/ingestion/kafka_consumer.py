# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

import asyncio
from typing import Callable
from ..utils.logger import get_logger
from ..settings import settings

logger = get_logger("kafka_consumer")

try:
    from aiokafka import AIOKafkaConsumer
except Exception:
    AIOKafkaConsumer = None
    logger.warning("aiokafka not installed; kafka consumer will not run in this environment.")


class KafkaIngestConsumer:
    def __init__(self, brokers: str = None, topic: str = None, handler: Callable[[str], None] = None):
        self.brokers = brokers or settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = topic or settings.KAFKA_TOPIC
        self.handler = handler or (lambda msg: logger.info("ingested: %s", msg))

    async def start(self):
        if AIOKafkaConsumer is None:
            logger.error("aiokafka not available. Install aiokafka to enable Kafka ingestion.")
            return
        consumer = AIOKafkaConsumer(self.topic, bootstrap_servers=self.brokers.split(","))
        await consumer.start()
        try:
            async for msg in consumer:
                text = msg.value.decode("utf-8")
                try:
                    self.handler(text)
                except Exception as e:
                    logger.exception("handler error: %s", e)
        finally:
            await consumer.stop()


# simple synchronous wrapper for testing
def simple_ingest_from_lines(lines, handler):
    for line in lines:
        handler(line)
