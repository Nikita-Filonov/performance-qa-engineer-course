from grpc.aio import ServicerContext

from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceServicer
from contracts.services.gateway.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.gateway.accounts.rpc_open_credit_card_account_pb2 import (
    OpenCreditCardAccountRequest,
    OpenCreditCardAccountResponse
)
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import (
    OpenDebitCardAccountRequest,
    OpenDebitCardAccountResponse
)
from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import (
    OpenDepositAccountRequest,
    OpenDepositAccountResponse
)
from contracts.services.gateway.accounts.rpc_open_savings_account_pb2 import (
    OpenSavingsAccountRequest,
    OpenSavingsAccountResponse
)
from services.accounts.clients.accounts.grpc import get_accounts_grpc_client
from services.cards.clients.cards.grpc import get_cards_grpc_client
from services.documents.services.kafka.producer import get_documents_kafka_producer_client
from services.gateway.apps.accounts.controllers.accounts.grpc import (
    get_accounts,
    open_deposit_account,
    open_savings_account,
    open_debit_card_account,
    open_credit_card_account
)
from services.users.clients.users.grpc import get_users_grpc_client


class AccountsGatewayService(AccountsGatewayServiceServicer):
    async def GetAccounts(self, request: GetAccountsRequest, context: ServicerContext) -> GetAccountsResponse:
        return await get_accounts(
            request,
            cards_grpc_client=get_cards_grpc_client(),
            accounts_grpc_client=get_accounts_grpc_client()
        )

    async def OpenDepositAccount(
            self,
            request: OpenDepositAccountRequest,
            context: ServicerContext
    ) -> OpenDepositAccountResponse:
        return await open_deposit_account(
            request,
            accounts_grpc_client=get_accounts_grpc_client(),
            documents_kafka_producer_client=get_documents_kafka_producer_client()
        )

    async def OpenSavingsAccount(
            self,
            request: OpenSavingsAccountRequest,
            context: ServicerContext
    ) -> OpenSavingsAccountResponse:
        return await open_savings_account(
            request,
            accounts_grpc_client=get_accounts_grpc_client(),
            documents_kafka_producer_client=get_documents_kafka_producer_client()
        )

    async def OpenDebitCardAccount(
            self,
            request: OpenDebitCardAccountRequest,
            context: ServicerContext
    ) -> OpenDebitCardAccountResponse:
        return await open_debit_card_account(
            context=context,
            request=request,
            users_grpc_client=get_users_grpc_client(),
            cards_grpc_client=get_cards_grpc_client(),
            accounts_grpc_client=get_accounts_grpc_client(),
            documents_kafka_producer_client=get_documents_kafka_producer_client()
        )

    async def OpenCreditCardAccount(
            self,
            request: OpenCreditCardAccountRequest,
            context: ServicerContext
    ) -> OpenCreditCardAccountResponse:
        return await open_credit_card_account(
            context=context,
            request=request,
            users_grpc_client=get_users_grpc_client(),
            cards_grpc_client=get_cards_grpc_client(),
            accounts_grpc_client=get_accounts_grpc_client(),
            documents_kafka_producer_client=get_documents_kafka_producer_client()
        )
