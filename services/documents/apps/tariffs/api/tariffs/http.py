import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.accounts.clients.accounts.http import AccountsHTTPClient, get_accounts_http_client
from services.documents.apps.tariffs.controllers.tariffs.http import get_tariff, create_tariff
from services.documents.apps.tariffs.schema.tariffs import GetTariffResponseSchema, CreateTariffRequestSchema, \
    CreateTariffResponseSchema
from services.documents.services.s3.client import get_documents_s3_client, DocumentsS3Client

tariffs_router = APIRouter(
    prefix=APIRoutes.TARIFFS,
    tags=[APIRoutes.TARIFFS.as_tag()]
)


@tariffs_router.get('/{account_id}', response_model=GetTariffResponseSchema)
async def get_tariff_view(
        account_id: uuid.UUID,
        documents_s3_client: Annotated[DocumentsS3Client, Depends(get_documents_s3_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)]
):
    return await get_tariff(
        account_id=account_id,
        documents_s3_client=documents_s3_client,
        accounts_http_client=accounts_http_client
    )


@tariffs_router.post('', response_model=CreateTariffResponseSchema)
async def create_tariff_view(
        request: CreateTariffRequestSchema,
        documents_s3_client: Annotated[DocumentsS3Client, Depends(get_documents_s3_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)]
):
    return await create_tariff(
        request=request,
        documents_s3_client=documents_s3_client,
        accounts_http_client=accounts_http_client
    )
