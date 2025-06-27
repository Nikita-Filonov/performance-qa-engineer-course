from services.documents.services.kafka.producer import TariffDocumentMessage
from services.documents.services.s3.client import DocumentsS3Client


def handle_tariff_documents(documents_s3_client: DocumentsS3Client):
    async def handle(message: str):
        tariff = TariffDocumentMessage.model_validate_json(message)

        await documents_s3_client.upload_tariff_file(
            data=tariff.content,
            account_id=tariff.account_id
        )

    return handle
