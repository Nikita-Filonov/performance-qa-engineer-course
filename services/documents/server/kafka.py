import asyncio

from services.documents.apps.contracts.controllers.contracts.kafka import handle_contract_documents
from services.documents.apps.receipts.controllers.receipts.kafka import handle_receipt_documents
from services.documents.apps.tariffs.controllers.tariffs.kafka import handle_tariff_documents
from services.documents.services.kafka.consumer import (
    get_documents_kafka_admin_client,
    get_documents_kafka_consumer_client
)
from services.documents.services.kafka.topics import DocumentsKafkaTopic
from services.documents.services.s3.client import get_documents_s3_client


async def consume():
    documents_s3_client = get_documents_s3_client()
    documents_kafka_admin_client = get_documents_kafka_admin_client()
    documents_kafka_consumer_client = get_documents_kafka_consumer_client()

    for topic in DocumentsKafkaTopic:
        documents_kafka_admin_client.create_topic(
            topic=topic,
            num_partitions=1,
            replication_factor=1
        )

    await asyncio.gather(
        documents_kafka_consumer_client.consume_tariff_documents(
            handler=handle_tariff_documents(documents_s3_client)
        ),
        documents_kafka_consumer_client.consume_receipt_documents(
            handler=handle_receipt_documents(documents_s3_client)
        ),
        documents_kafka_consumer_client.consume_contract_documents(
            handler=handle_contract_documents(documents_s3_client)
        ),
    )


if __name__ == '__main__':
    asyncio.run(consume())
