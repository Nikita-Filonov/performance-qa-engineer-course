import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.accounts.clients.accounts.http import AccountsHTTPClient, get_accounts_http_client
from services.documents.apps.contracts.controllers.contracts.http import create_contract, get_contract
from services.documents.apps.contracts.schema.contracts import (
    GetContractResponseSchema,
    CreateContractRequestSchema,
    CreateContractResponseSchema
)
from services.documents.services.s3.client import get_documents_s3_client, DocumentsS3Client

contracts_router = APIRouter(
    prefix=APIRoutes.CONTRACTS,
    tags=[APIRoutes.CONTRACTS.as_tag()]
)


@contracts_router.get('/{account_id}', response_model=GetContractResponseSchema)
async def get_contract_view(
        account_id: uuid.UUID,
        documents_s3_client: Annotated[DocumentsS3Client, Depends(get_documents_s3_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)]
):
    return await get_contract(
        account_id=account_id,
        documents_s3_client=documents_s3_client,
        accounts_http_client=accounts_http_client
    )


@contracts_router.post('', response_model=CreateContractResponseSchema)
async def create_contract_view(
        request: CreateContractRequestSchema,
        documents_s3_client: Annotated[DocumentsS3Client, Depends(get_documents_s3_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)]
):
    return await create_contract(
        request=request,
        documents_s3_client=documents_s3_client,
        accounts_http_client=accounts_http_client
    )
