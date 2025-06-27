from config import settings
from libs.kafka.admin import KafkaAdminClient
from libs.kafka.consumer import KafkaConsumerClient, KafkaConsumerHandler
from libs.logger import get_logger
from services.documents.services.kafka.topics import DocumentsKafkaTopic


class DocumentsKafkaConsumerClient(KafkaConsumerClient):
    async def consume_tariff_documents(self, handler: KafkaConsumerHandler):
        await self.start(
            topic=DocumentsKafkaTopic.TARIFFS_INBOX,
            group_id="documents-tariffs-group",
            handler=handler
        )

    async def consume_receipt_documents(self, handler: KafkaConsumerHandler):
        await self.start(
            topic=DocumentsKafkaTopic.RECEIPTS_INBOX,
            group_id="documents-receipts-group",
            handler=handler
        )

    async def consume_contract_documents(self, handler: KafkaConsumerHandler):
        await self.start(
            topic=DocumentsKafkaTopic.CONTRACTS_INBOX,
            group_id="documents-contracts-group",
            handler=handler
        )


def get_documents_kafka_admin_client() -> KafkaAdminClient:
    logger = get_logger("DOCUMENTS_KAFKA_ADMIN_CLIENT")
    return KafkaAdminClient(config=settings.documents_kafka_client, logger=logger)


def get_documents_kafka_consumer_client() -> DocumentsKafkaConsumerClient:
    logger = get_logger("DOCUMENTS_KAFKA_CONSUMER_CLIENT")
    return DocumentsKafkaConsumerClient(config=settings.documents_kafka_client, logger=logger)
