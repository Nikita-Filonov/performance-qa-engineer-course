import asyncio

from grpc_reflection.v1alpha import reflection

from config import settings
from contracts.services.accounts import accounts_service_pb2
from contracts.services.accounts import accounts_service_pb2_grpc
from libs.grpc.server.base import build_grpc_server
from libs.logger import get_logger
from services.accounts.apps.accounts.api.accounts.grpc import AccountsService


async def serve():
    logger = get_logger("ACCOUNTS_SERVICE_GRPC_SERVER")
    server = build_grpc_server(settings.accounts_grpc_server, logger)

    accounts_service_pb2_grpc.add_AccountsServiceServicer_to_server(AccountsService(), server)

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            accounts_service_pb2.DESCRIPTOR.services_by_name['AccountsService'].full_name,
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
