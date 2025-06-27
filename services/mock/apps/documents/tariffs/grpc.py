from grpc.aio import ServicerContext

from contracts.services.documents.tariffs.rpc_create_tariff_pb2 import CreateTariffRequest, CreateTariffResponse
from contracts.services.documents.tariffs.rpc_get_tariff_pb2 import GetTariffRequest, GetTariffResponse
from contracts.services.documents.tariffs.tariffs_service_pb2_grpc import TariffsServiceServicer
from services.mock.apps.documents.tariffs.mock import loader


class TariffsMockService(TariffsServiceServicer):
    async def GetTariff(self, request: GetTariffRequest, context: ServicerContext) -> GetTariffResponse:
        return await loader.load_grpc_with_timeout("GetTariff/default.json", GetTariffResponse)

    async def CreateTariff(self, request: CreateTariffRequest, context: ServicerContext) -> CreateTariffResponse:
        return await loader.load_grpc_with_timeout("CreateTariff/default.json", CreateTariffResponse)
