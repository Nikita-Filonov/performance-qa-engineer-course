from config import settings
from libs.logger import get_logger
from libs.s3.client import S3Client, S3File


def build_tariff_file_key(account_id: str) -> str:
    return f'tariff_{account_id}.pdf'


def build_contract_file_key(account_id: str) -> str:
    return f'contract_{account_id}.pdf'


class DocumentsS3Client(S3Client):
    async def get_tariff_file(self, account_id: str) -> S3File:
        return await self.get_file(key=build_tariff_file_key(account_id))

    async def upload_tariff_file(self, account_id: str, data: bytes) -> S3File:
        key = build_tariff_file_key(account_id)

        await self.upload_file(key=key, data=data)
        return await self.get_file(key=key)

    async def get_contract_file(self, account_id: str) -> S3File:
        return await self.get_file(key=build_contract_file_key(account_id))

    async def upload_contract_file(self, account_id: str, data: bytes) -> S3File:
        key = build_contract_file_key(account_id)

        await self.upload_file(key=key, data=data)
        return await self.get_file(key=key)


def get_documents_s3_client() -> DocumentsS3Client:
    logger = get_logger("DOCUMENTS_S3_CLIENT")
    return DocumentsS3Client(config=settings.documents_s3_client, logger=logger)
