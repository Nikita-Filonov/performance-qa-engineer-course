from grpc.aio import ServicerContext

from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import CardsGatewayServiceServicer
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardRequest,
    IssuePhysicalCardResponse
)
from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import (
    IssueVirtualCardRequest,
    IssueVirtualCardResponse
)
from services.cards.clients.cards.grpc import get_cards_grpc_client
from services.gateway.apps.cards.controllers.cards.grpc import issue_virtual_card, issue_physical_card
from services.users.clients.users.grpc import get_users_grpc_client


class CardsGatewayService(CardsGatewayServiceServicer):
    async def IssueVirtualCard(
            self,
            request: IssuePhysicalCardRequest,
            context: ServicerContext
    ) -> IssuePhysicalCardResponse:
        return await issue_virtual_card(
            context=context,
            request=request,
            cards_grpc_client=get_cards_grpc_client(),
            users_grpc_client=get_users_grpc_client()
        )

    async def IssuePhysicalCard(
            self,
            request: IssueVirtualCardRequest,
            context: ServicerContext
    ) -> IssueVirtualCardResponse:
        return await issue_physical_card(
            context=context,
            request=request,
            cards_grpc_client=get_cards_grpc_client(),
            users_grpc_client=get_users_grpc_client()
        )
