from grpc.aio import ServicerContext

from contracts.services.documents.tariffs.rpc_create_tariff_pb2 import CreateTariffRequest, CreateTariffResponse
from contracts.services.documents.tariffs.rpc_get_tariff_pb2 import GetTariffRequest, GetTariffResponse
from contracts.services.documents.tariffs.tariffs_service_pb2_grpc import TariffsServiceServicer
from services.accounts.clients.accounts.grpc import get_accounts_grpc_client
from services.documents.apps.tariffs.controllers.tariffs.grpc import get_tariff, create_tariff
from services.documents.services.s3.client import get_documents_s3_client


class TariffsService(TariffsServiceServicer):
    async def GetTariff(self, request: GetTariffRequest, context: ServicerContext) -> GetTariffResponse:
        return await get_tariff(
            context=context,
            request=request,
            documents_s3_client=get_documents_s3_client(),
            accounts_grpc_client=get_accounts_grpc_client()
        )

    async def CreateTariff(self, request: CreateTariffRequest, context: ServicerContext) -> CreateTariffResponse:
        return await create_tariff(
            context=context,
            request=request,
            documents_s3_client=get_documents_s3_client(),
            accounts_grpc_client=get_accounts_grpc_client()
        )
