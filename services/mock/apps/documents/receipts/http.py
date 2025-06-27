import uuid

from fastapi import APIRouter

from libs.routes import APIRoutes
from services.documents.apps.receipts.schema.receipts import (
    GetReceiptResponseSchema,
    CreateReceiptRequestSchema,
    CreateReceiptResponseSchema
)
from services.mock.apps.documents.receipts.mock import loader

receipts_mock_router = APIRouter(
    prefix=APIRoutes.RECEIPTS,
    tags=[APIRoutes.RECEIPTS.as_tag()]
)


@receipts_mock_router.get('/{operation_id}', response_model=GetReceiptResponseSchema)
async def get_receipt_view(operation_id: uuid.UUID):
    return loader.load_http("get_receipt/default.json", GetReceiptResponseSchema)


@receipts_mock_router.post('', response_model=CreateReceiptResponseSchema)
async def create_receipt_view(request: CreateReceiptRequestSchema):
    return loader.load_http("create_receipt/default.json", CreateReceiptResponseSchema)
