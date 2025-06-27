import asyncio

from grpc_reflection.v1alpha import reflection

from config import settings
from contracts.services.documents.contracts import contracts_service_pb2
from contracts.services.documents.contracts import contracts_service_pb2_grpc
from contracts.services.documents.receipts import receipts_service_pb2
from contracts.services.documents.receipts import receipts_service_pb2_grpc
from contracts.services.documents.tariffs import tariffs_service_pb2
from contracts.services.documents.tariffs import tariffs_service_pb2_grpc
from libs.grpc.server.base import build_grpc_server
from libs.logger import get_logger
from services.documents.apps.contracts.api.contracts.grpc import ContractsService
from services.documents.apps.receipts.api.receipts.grpc import ReceiptsService
from services.documents.apps.tariffs.api.tariffs.grpc import TariffsService


async def serve():
    logger = get_logger("DOCUMENTS_SERVICE_GRPC_SERVER")
    server = build_grpc_server(settings.documents_grpc_server, logger)

    tariffs_service_pb2_grpc.add_TariffsServiceServicer_to_server(TariffsService(), server)
    receipts_service_pb2_grpc.add_ReceiptsServiceServicer_to_server(ReceiptsService(), server)
    contracts_service_pb2_grpc.add_ContractsServiceServicer_to_server(ContractsService(), server)

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            tariffs_service_pb2.DESCRIPTOR.services_by_name['TariffsService'].full_name,
            receipts_service_pb2.DESCRIPTOR.services_by_name['ReceiptsService'].full_name,
            contracts_service_pb2.DESCRIPTOR.services_by_name['ContractsService'].full_name,
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
