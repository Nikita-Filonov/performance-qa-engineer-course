from config import settings
from libs.logger import get_logger
from libs.s3.client import S3Client, S3File


def build_operation_receipt_file_key(operation_id: str) -> str:
    return f'operation_receipt_{operation_id}.pdf'


class OperationsS3Client(S3Client):
    async def get_operation_receipt_file(self, operation_id: str) -> S3File:
        return await self.get_file(key=build_operation_receipt_file_key(operation_id))

    async def upload_operation_receipt_file(self, operation_id: str, data: bytes) -> S3File:
        key = build_operation_receipt_file_key(operation_id)

        await self.upload_file(key=key, data=data)
        return await self.get_file(key=key)


def get_operations_s3_client() -> OperationsS3Client:
    logger = get_logger("OPERATIONS_S3_CLIENT")
    return OperationsS3Client(config=settings.operations_s3_client, logger=logger)
