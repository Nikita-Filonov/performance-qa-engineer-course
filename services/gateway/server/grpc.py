import asyncio

from grpc_reflection.v1alpha import reflection

from config import settings
from contracts.services.gateway.accounts import accounts_gateway_service_pb2
from contracts.services.gateway.accounts import accounts_gateway_service_pb2_grpc
from contracts.services.gateway.cards import cards_gateway_service_pb2
from contracts.services.gateway.cards import cards_gateway_service_pb2_grpc
from contracts.services.gateway.documents import documents_gateway_service_pb2
from contracts.services.gateway.documents import documents_gateway_service_pb2_grpc
from contracts.services.gateway.operations import operations_gateway_service_pb2
from contracts.services.gateway.operations import operations_gateway_service_pb2_grpc
from contracts.services.gateway.users import users_gateway_service_pb2
from contracts.services.gateway.users import users_gateway_service_pb2_grpc
from libs.grpc.server.base import build_grpc_server
from libs.logger import get_logger
from services.gateway.apps.accounts.api.accounts.grpc import AccountsGatewayService
from services.gateway.apps.cards.api.cards.grpc import CardsGatewayService
from services.gateway.apps.documents.api.documents.grpc import DocumentsGatewayService
from services.gateway.apps.operations.api.operations.grpc import OperationsGatewayService
from services.gateway.apps.users.api.users.grpc import UsersGatewayService


async def serve():
    logger = get_logger("GATEWAY_SERVICE_GRPC_SERVER")
    server = build_grpc_server(settings.gateway_grpc_server, logger)

    users_gateway_service_pb2_grpc.add_UsersGatewayServiceServicer_to_server(
        UsersGatewayService(), server
    )
    cards_gateway_service_pb2_grpc.add_CardsGatewayServiceServicer_to_server(
        CardsGatewayService(), server
    )
    accounts_gateway_service_pb2_grpc.add_AccountsGatewayServiceServicer_to_server(
        AccountsGatewayService(), server
    )
    documents_gateway_service_pb2_grpc.add_DocumentsGatewayServiceServicer_to_server(
        DocumentsGatewayService(), server
    )
    operations_gateway_service_pb2_grpc.add_OperationsGatewayServiceServicer_to_server(
        OperationsGatewayService(), server
    )

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            users_gateway_service_pb2.DESCRIPTOR.services_by_name['UsersGatewayService'].full_name,
            cards_gateway_service_pb2.DESCRIPTOR.services_by_name['CardsGatewayService'].full_name,
            accounts_gateway_service_pb2.DESCRIPTOR.services_by_name['AccountsGatewayService'].full_name,
            documents_gateway_service_pb2.DESCRIPTOR.services_by_name['DocumentsGatewayService'].full_name,
            operations_gateway_service_pb2.DESCRIPTOR.services_by_name['OperationsGatewayService'].full_name,
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
