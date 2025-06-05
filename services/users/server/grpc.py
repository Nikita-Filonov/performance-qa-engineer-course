import asyncio

from grpc_reflection.v1alpha import reflection

from config import settings
from contracts.services.users import users_service_pb2
from contracts.services.users import users_service_pb2_grpc
from libs.grpc.server.base import build_grpc_server
from libs.logger import get_logger
from services.users.apps.users.api.users.grpc import UsersService


async def serve():
    logger = get_logger("USERS_SERVICE_GRPC_SERVER")
    server = build_grpc_server(settings.users_grpc_server, logger)

    users_service_pb2_grpc.add_UsersServiceServicer_to_server(UsersService(), server)

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            users_service_pb2.DESCRIPTOR.services_by_name['UsersService'].full_name,
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
