import uuid

from fastapi import HTTPException, status
from pydantic import HttpUrl

from libs.s3.client import S3File
from services.accounts.clients.accounts.http import AccountsHTTPClient, AccountsHTTPClientError
from services.documents.apps.tariffs.schema.tariffs import (
    TariffSchema,
    GetTariffResponseSchema,
    CreateTariffRequestSchema,
    CreateTariffResponseSchema
)
from services.documents.services.s3.client import DocumentsS3Client


def build_tariff_from_file(file: S3File) -> TariffSchema:
    return TariffSchema(url=HttpUrl(file.url), document=file.content)


async def get_tariff(
        account_id: uuid.UUID,
        documents_s3_client: DocumentsS3Client,
        accounts_http_client: AccountsHTTPClient,
) -> GetTariffResponseSchema:
    try:
        get_account_response = await accounts_http_client.get_account(account_id)
    except AccountsHTTPClientError as error:
        raise HTTPException(
            detail=f"Get tariff: {error.details}",
            status_code=error.status_code
        )

    try:
        file = await documents_s3_client.get_tariff_file(get_account_response.account.id)
    except Exception as error:
        raise HTTPException(
            detail=f"Get tariff: {error}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return GetTariffResponseSchema(tariff=build_tariff_from_file(file))


async def create_tariff(
        request: CreateTariffRequestSchema,
        documents_s3_client: DocumentsS3Client,
        accounts_http_client: AccountsHTTPClient,
) -> CreateTariffResponseSchema:
    try:
        get_account_response = await accounts_http_client.get_account(request.account_id)
    except AccountsHTTPClientError as error:
        raise HTTPException(
            detail=f"Create tariff: {error.details}",
            status_code=error.status_code
        )

    file = await documents_s3_client.upload_tariff_file(
        get_account_response.account.id, request.content
    )

    return CreateTariffResponseSchema(tariff=build_tariff_from_file(file))
