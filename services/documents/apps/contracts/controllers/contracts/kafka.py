from services.documents.services.kafka.producer import ContractDocumentMessage
from services.documents.services.s3.client import DocumentsS3Client


def handle_contract_documents(documents_s3_client: DocumentsS3Client):
    async def handle(message: str):
        contract = ContractDocumentMessage.model_validate_json(message)

        await documents_s3_client.upload_contract_file(
            data=contract.content,
            account_id=contract.account_id
        )

    return handle
