from grpc.aio import AioRpcError, ServicerContext

from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardRequest,
    IssuePhysicalCardResponse
)
from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import (
    IssueVirtualCardRequest,
    IssueVirtualCardResponse
)
from services.cards.clients.cards.grpc import CardsGRPCClient
from services.users.clients.users.grpc import UsersGRPCClient


async def issue_virtual_card(
        context: ServicerContext,
        request: IssueVirtualCardRequest,
        users_grpc_client: UsersGRPCClient,
        cards_grpc_client: CardsGRPCClient
) -> IssueVirtualCardResponse:
    try:
        user = await users_grpc_client.get_user(request.user_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Issue virtual card: {error.details()}"
        )

    card = await cards_grpc_client.create_virtual_card(
        last_name=user.last_name,
        first_name=user.first_name,
        account_id=request.account_id
    )

    return IssueVirtualCardResponse(card=card)


async def issue_physical_card(
        context: ServicerContext,
        request: IssuePhysicalCardRequest,
        users_grpc_client: UsersGRPCClient,
        cards_grpc_client: CardsGRPCClient
) -> IssuePhysicalCardResponse:
    try:
        user = await users_grpc_client.get_user(request.user_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Issue physical card: {error.details()}"
        )

    card = await cards_grpc_client.create_physical_card(
        last_name=user.last_name,
        first_name=user.first_name,
        account_id=request.account_id
    )

    return IssuePhysicalCardResponse(card=card)
