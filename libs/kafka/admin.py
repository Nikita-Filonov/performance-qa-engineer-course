from logging import Logger

from confluent_kafka.admin import AdminClient, NewTopic

from libs.config.kafka import KafkaClientConfig


class KafkaAdminClient:
    def __init__(self, config: KafkaClientConfig, logger: Logger):
        self.admin = AdminClient({'bootstrap.servers': config.bootstrap_servers})
        self.logger = logger

    def create_topic(self, topic: str, num_partitions: int = 1, replication_factor: int = 1):
        new_topic = NewTopic(
            topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        futures = self.admin.create_topics([new_topic])

        for topic_name, future in futures.items():
            try:
                future.result()
                self.logger.info(f"Kafka topic '{topic_name}' created")
            except Exception as error:
                if "TopicExistsError" in str(error):
                    self.logger.info(f"Topic '{topic_name}' already exists")
                else:
                    self.logger.error(f"Failed to create topic '{topic_name}': {error}")
