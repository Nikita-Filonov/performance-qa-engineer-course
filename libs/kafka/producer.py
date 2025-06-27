from logging import Logger

from aiokafka import AIOKafkaProducer

from libs.config.kafka import KafkaClientConfig


class KafkaProducerClient:
    def __init__(self, config: KafkaClientConfig, logger: Logger):
        self.logger = logger
        self.config = config
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.config.bootstrap_servers)

        try:
            await self.producer.start()
            self.logger.info("Kafka producer started")
        except Exception as error:
            self.logger.exception(f"Failed to start Kafka producer: {error}")
            await self.stop()

            raise error

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            self.logger.info("Kafka producer stopped")

    async def produce(self, topic: str, value: str):
        if not self.producer:
            raise RuntimeError("Kafka producer is not started")

        try:
            await self.producer.send_and_wait(topic, value.encode("utf-8"))
            self.logger.info(f"Message sent to topic '{topic}'")
        except Exception as error:
            self.logger.exception(f"Failed to send message to topic '{topic}': {error}")
