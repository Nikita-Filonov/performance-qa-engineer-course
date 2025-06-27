import uuid

from fastapi import HTTPException, status
from pydantic import HttpUrl

from libs.s3.client import S3File
from services.accounts.clients.accounts.http import AccountsHTTPClient, AccountsHTTPClientError
from services.documents.apps.contracts.schema.contracts import (
    ContractSchema,
    GetContractResponseSchema,
    CreateContractRequestSchema,
    CreateContractResponseSchema,
)
from services.documents.services.s3.client import DocumentsS3Client


def build_contract_from_file(file: S3File) -> ContractSchema:
    return ContractSchema(url=HttpUrl(file.url), document=file.content)


async def get_contract(
        account_id: uuid.UUID,
        documents_s3_client: DocumentsS3Client,
        accounts_http_client: AccountsHTTPClient,
) -> GetContractResponseSchema:
    try:
        get_account_response = await accounts_http_client.get_account(account_id)
    except AccountsHTTPClientError as error:
        raise HTTPException(
            detail=f"Get contract: {error.details}",
            status_code=error.status_code
        )

    try:
        file = await documents_s3_client.get_contract_file(get_account_response.account.id)
    except Exception as error:
        raise HTTPException(
            detail=f"Get contract: {error}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return GetContractResponseSchema(contract=build_contract_from_file(file))


async def create_contract(
        request: CreateContractRequestSchema,
        documents_s3_client: DocumentsS3Client,
        accounts_http_client: AccountsHTTPClient,
) -> CreateContractResponseSchema:
    try:
        get_account_response = await accounts_http_client.get_account(request.account_id)
    except AccountsHTTPClientError as error:
        raise HTTPException(
            detail=f"Create contract: {error.details}",
            status_code=error.status_code
        )

    file = await documents_s3_client.upload_contract_file(
        get_account_response.account.id, request.content
    )

    return CreateContractResponseSchema(contract=build_contract_from_file(file))
