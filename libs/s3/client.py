import json
from dataclasses import dataclass
from logging import Logger

from aioboto3 import Session
from botocore.exceptions import ClientError

from libs.config.s3 import S3ClientConfig


@dataclass
class S3File:
    url: str
    content: bytes


class S3Client:
    def __init__(self, config: S3ClientConfig, logger: Logger):
        self.config = config
        self.logger = logger
        self.session = Session()

    def get_client(self):
        return self.session.client(
            "s3",
            region_name="us-east-1",
            endpoint_url=str(self.config.internal_url),
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
        )

    async def create_public_bucket(self):
        public_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{self.config.bucket}/*"]
                }
            ]
        }

        async with self.get_client() as s3:
            await s3.create_bucket(Bucket=self.config.bucket)
            await s3.put_bucket_policy(
                Bucket=self.config.bucket,
                Policy=json.dumps(public_policy),
            )

    async def ensure_bucket_exists(self):
        async with self.get_client() as s3:
            try:
                await s3.head_bucket(Bucket=self.config.bucket)
                self.logger.debug(f"Bucket '{self.config.bucket}' already exists.")
            except s3.exceptions.ClientError:
                self.logger.warning(f"Bucket '{self.config.bucket}' not found. Creating...")
                await self.create_public_bucket()
                self.logger.info(f"Bucket '{self.config.bucket}' created.")

    async def get_file(self, key: str) -> S3File:
        await self.ensure_bucket_exists()

        self.logger.info(f"Downloading file from S3: bucket={self.config.bucket}, key={key}")

        try:
            async with self.get_client() as s3:
                file = await s3.get_object(Bucket=self.config.bucket, Key=key)
                content = await file["Body"].read()
                self.logger.info(f"Successfully downloaded file: {key}")
                return S3File(url=self.config.get_file_url(key), content=content)
        except ClientError as error:
            self.logger.exception(f"Failed to download file {key}: {error}")
            raise error

    async def list_files(self, prefix: str = "") -> list[str]:
        await self.ensure_bucket_exists()

        self.logger.info(f"Listing files in bucket={self.config.bucket} with prefix='{prefix}'")

        try:
            async with self.get_client() as s3:
                response = await s3.list_objects_v2(Bucket=self.config.bucket, Prefix=prefix)
                contents = response.get("Contents", [])
                keys = [obj["Key"] for obj in contents]
                self.logger.info(f"Found {len(keys)} file(s) with prefix='{prefix}'")
                return keys
        except ClientError as error:
            self.logger.exception(f"Failed to list files: {error}")
            raise error

    async def upload_file(self, key: str, data: bytes) -> None:
        await self.ensure_bucket_exists()

        self.logger.info(f"Uploading file to S3: bucket={self.config.bucket}, key={key}")

        try:
            async with self.get_client() as s3:
                await s3.put_object(Bucket=self.config.bucket, Key=key, Body=data)
                self.logger.info(f"Successfully uploaded file: {key}")
        except ClientError as error:
            self.logger.exception(f"Failed to upload file {key}: {error}")
            raise error

    async def delete_file(self, key: str):
        await self.ensure_bucket_exists()

        self.logger.info(f"Deleting file from S3: bucket={self.config.bucket}, key={key}")

        try:
            async with self.get_client() as s3:
                await s3.delete_object(Bucket=self.config.bucket, Key=key)
                self.logger.info(f"Successfully deleted file: {key}")
        except ClientError as error:
            self.logger.exception(f"Failed to delete file {key}: {error}")
            raise error
