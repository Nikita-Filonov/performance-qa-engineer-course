from pydantic import BaseModel, UUID4

from config import settings
from libs.kafka.producer import KafkaProducerClient
from libs.logger import get_logger
from services.documents.services.kafka.topics import DocumentsKafkaTopic


class TariffDocumentMessage(BaseModel):
    content: bytes
    account_id: UUID4


class ReceiptDocumentMessage(BaseModel):
    content: bytes
    operation_id: UUID4


class ContractDocumentMessage(BaseModel):
    content: bytes
    account_id: UUID4


class DocumentsKafkaProducerClient(KafkaProducerClient):
    async def produce_tariff_document_api(self, message: TariffDocumentMessage):
        await self.start()
        await self.produce(
            topic=DocumentsKafkaTopic.TARIFFS_INBOX,
            value=message.model_dump_json()
        )
        await self.stop()

    async def produce_receipt_document_api(self, message: ReceiptDocumentMessage):
        await self.start()
        await self.produce(
            topic=DocumentsKafkaTopic.RECEIPTS_INBOX,
            value=message.model_dump_json()
        )
        await self.stop()

    async def produce_contract_document_api(self, message: ContractDocumentMessage):
        await self.start()
        await self.produce(
            topic=DocumentsKafkaTopic.CONTRACTS_INBOX,
            value=message.model_dump_json()
        )
        await self.stop()

    async def produce_tariff_document(self, content: bytes, account_id: str):
        message = TariffDocumentMessage(
            content=content,
            account_id=account_id
        )
        await self.produce_tariff_document_api(message)

    async def produce_receipt_document(self, content: bytes, operation_id: str):
        message = ReceiptDocumentMessage(
            content=content,
            operation_id=operation_id
        )
        await self.produce_receipt_document_api(message)

    async def produce_contract_document(self, content: bytes, account_id: str):
        message = ContractDocumentMessage(
            content=content,
            account_id=account_id
        )
        await self.produce_contract_document_api(message)


def get_documents_kafka_producer_client() -> DocumentsKafkaProducerClient:
    logger = get_logger("DOCUMENTS_KAFKA_PRODUCER_CLIENT")
    return DocumentsKafkaProducerClient(config=settings.documents_kafka_client, logger=logger)
