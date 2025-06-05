import asyncio

from grpc_reflection.v1alpha import reflection

from config import settings
from contracts.services.cards import cards_service_pb2
from contracts.services.cards import cards_service_pb2_grpc
from libs.grpc.server.base import build_grpc_server
from libs.logger import get_logger
from services.cards.apps.cards.api.cards.grpc import CardsService


async def serve():
    logger = get_logger("CARDS_SERVICE_GRPC_SERVER")
    server = build_grpc_server(settings.cards_grpc_server, logger)

    cards_service_pb2_grpc.add_CardsServiceServicer_to_server(CardsService(), server)

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            cards_service_pb2.DESCRIPTOR.services_by_name['CardsService'].full_name,
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
