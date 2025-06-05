from config import settings
from contracts.services.documents.tariffs.rpc_create_tariff_pb2 import CreateTariffRequest, CreateTariffResponse
from contracts.services.documents.tariffs.rpc_get_tariff_pb2 import GetTariffRequest, GetTariffResponse
from contracts.services.documents.tariffs.tariff_pb2 import Tariff
from contracts.services.documents.tariffs.tariffs_service_pb2_grpc import TariffsServiceStub
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger


class TariffsGRPCClient(GRPCClient):
    stub: TariffsServiceStub
    stub_class = TariffsServiceStub

    async def get_tariff_api(self, request: GetTariffRequest) -> GetTariffResponse:
        return await self.stub.GetTariff(request)

    async def create_tariff_api(self, request: CreateTariffRequest) -> CreateTariffResponse:
        return await self.stub.CreateTariff(request)

    async def get_tariff(self, account_id: str) -> Tariff:
        request = GetTariffRequest(account_id=account_id)
        response = await self.get_tariff_api(request)
        return response.tariff

    async def create_tariff(self, account_id: str, content: bytes) -> Tariff:
        request = CreateTariffRequest(account_id=account_id, content=content)
        response = await self.create_tariff_api(request)
        return response.tariff


def get_tariffs_grpc_client() -> TariffsGRPCClient:
    logger = get_logger("TARIFFS_SERVICE_GRPC_CLIENT")
    return TariffsGRPCClient(config=settings.documents_grpc_client, logger=logger)
