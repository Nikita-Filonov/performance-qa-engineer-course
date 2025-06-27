import uuid

from fastapi import APIRouter

from libs.routes import APIRoutes
from services.documents.apps.tariffs.schema.tariffs import (
    GetTariffResponseSchema,
    CreateTariffRequestSchema,
    CreateTariffResponseSchema
)
from services.mock.apps.documents.tariffs.mock import loader

tariffs_mock_router = APIRouter(
    prefix=APIRoutes.TARIFFS,
    tags=[APIRoutes.TARIFFS.as_tag()]
)


@tariffs_mock_router.get('/{account_id}', response_model=GetTariffResponseSchema)
async def get_tariff_view(account_id: uuid.UUID):
    return await loader.load_http_with_timeout("get_tariff/default.json", GetTariffResponseSchema)


@tariffs_mock_router.post('', response_model=CreateTariffResponseSchema)
async def create_tariff_view(request: CreateTariffRequestSchema):
    return await loader.load_http_with_timeout("create_tariff/default.json", CreateTariffResponseSchema)
