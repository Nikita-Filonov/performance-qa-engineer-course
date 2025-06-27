from logging import Logger
from typing import Callable, Awaitable

from aiokafka import AIOKafkaConsumer

from libs.config.kafka import KafkaClientConfig

KafkaConsumerHandler = Callable[[str], Awaitable[None]]


class KafkaConsumerClient:
    def __init__(self, config: KafkaClientConfig, logger: Logger):
        self.config = config
        self.logger = logger

    async def start(self, topic: str, group_id: str, handler: KafkaConsumerHandler):
        consumer = AIOKafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=self.config.bootstrap_servers,
        )
        await consumer.start()
        self.logger.info(f"Kafka consumer started for topic '{topic}'")

        try:
            async for message in consumer:
                message = message.value.decode("utf-8")
                self.logger.info(f"Received message: {message}")
                await handler(message)
        finally:
            await consumer.stop()
            self.logger.info("Kafka consumer stopped")
