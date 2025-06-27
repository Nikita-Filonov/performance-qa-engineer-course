from services.documents.services.kafka.producer import ReceiptDocumentMessage
from services.documents.services.s3.client import DocumentsS3Client


def handle_receipt_documents(documents_s3_client: DocumentsS3Client):
    async def handle(message: str):
        receipt = ReceiptDocumentMessage.model_validate_json(message)

        await documents_s3_client.upload_receipt_file(
            data=receipt.content,
            operation_id=receipt.operation_id
        )

    return handle
