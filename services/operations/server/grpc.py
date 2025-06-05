import asyncio

from grpc_reflection.v1alpha import reflection

from config import settings
from contracts.services.operations import operations_service_pb2
from contracts.services.operations import operations_service_pb2_grpc
from libs.grpc.server.base import build_grpc_server
from libs.logger import get_logger
from services.operations.apps.operations.api.operations.grpc import OperationsService


async def serve():
    logger = get_logger("OPERATIONS_SERVICE_GRPC_SERVER")
    server = build_grpc_server(settings.operations_grpc_server, logger)

    operations_service_pb2_grpc.add_OperationsServiceServicer_to_server(OperationsService(), server)

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            operations_service_pb2.DESCRIPTOR.services_by_name['OperationsService'].full_name,
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
