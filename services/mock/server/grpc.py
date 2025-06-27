import asyncio

from grpc_reflection.v1alpha import reflection

from config import settings
from contracts.services.accounts import accounts_service_pb2
from contracts.services.accounts import accounts_service_pb2_grpc
from contracts.services.cards import cards_service_pb2
from contracts.services.cards import cards_service_pb2_grpc
from contracts.services.documents.contracts import contracts_service_pb2
from contracts.services.documents.contracts import contracts_service_pb2_grpc
from contracts.services.documents.receipts import receipts_service_pb2
from contracts.services.documents.receipts import receipts_service_pb2_grpc
from contracts.services.documents.tariffs import tariffs_service_pb2
from contracts.services.documents.tariffs import tariffs_service_pb2_grpc
from contracts.services.operations import operations_service_pb2
from contracts.services.operations import operations_service_pb2_grpc
from contracts.services.users import users_service_pb2
from contracts.services.users import users_service_pb2_grpc
from libs.grpc.server.base import build_grpc_server
from libs.logger import get_logger
from services.mock.apps.accounts.grpc import AccountsMockService
from services.mock.apps.cards.grpc import CardsMockService
from services.mock.apps.documents.contracts.grpc import ContractsMockService
from services.mock.apps.documents.receipts.grpc import ReceiptsMockService
from services.mock.apps.documents.tariffs.grpc import TariffsMockService
from services.mock.apps.operations.grpc import OperationsMockService
from services.mock.apps.users.grpc import UsersMockService


async def serve():
    logger = get_logger("MOCK_SERVICE_GRPC_SERVER")
    server = build_grpc_server(settings.mock_grpc_server, logger)

    users_service_pb2_grpc.add_UsersServiceServicer_to_server(UsersMockService(), server)
    cards_service_pb2_grpc.add_CardsServiceServicer_to_server(CardsMockService(), server)
    tariffs_service_pb2_grpc.add_TariffsServiceServicer_to_server(TariffsMockService(), server)
    receipts_service_pb2_grpc.add_ReceiptsServiceServicer_to_server(ReceiptsMockService(), server)
    accounts_service_pb2_grpc.add_AccountsServiceServicer_to_server(AccountsMockService(), server)
    contracts_service_pb2_grpc.add_ContractsServiceServicer_to_server(ContractsMockService(), server)
    operations_service_pb2_grpc.add_OperationsServiceServicer_to_server(OperationsMockService(), server)

    reflection.enable_server_reflection(
        (
            reflection.SERVICE_NAME,
            users_service_pb2.DESCRIPTOR.services_by_name['UsersService'].full_name,
            cards_service_pb2.DESCRIPTOR.services_by_name['CardsService'].full_name,
            tariffs_service_pb2.DESCRIPTOR.services_by_name['TariffsService'].full_name,
            receipts_service_pb2.DESCRIPTOR.services_by_name['ReceiptsService'].full_name,
            accounts_service_pb2.DESCRIPTOR.services_by_name['AccountsService'].full_name,
            contracts_service_pb2.DESCRIPTOR.services_by_name['ContractsService'].full_name,
            operations_service_pb2.DESCRIPTOR.services_by_name['OperationsService'].full_name
        ),
        server
    )

    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve())
