from grpc import StatusCode
from grpc.aio import AioRpcError, ServicerContext

from contracts.services.documents.contracts.contract_pb2 import Contract
from contracts.services.documents.contracts.rpc_create_contract_pb2 import CreateContractRequest, CreateContractResponse
from contracts.services.documents.contracts.rpc_get_contract_pb2 import GetContractRequest, GetContractResponse
from libs.s3.client import S3File
from services.accounts.clients.accounts.grpc import AccountsGRPCClient
from services.documents.services.s3.client import DocumentsS3Client


def build_contract_from_file(file: S3File) -> Contract:
    return Contract(url=file.url, document=file.content)


async def get_contract(
        context: ServicerContext,
        request: GetContractRequest,
        documents_s3_client: DocumentsS3Client,
        accounts_grpc_client: AccountsGRPCClient,
) -> GetContractResponse:
    try:
        account = await accounts_grpc_client.get_account(request.account_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Get contract: {error.details()}"
        )

    try:
        file = await documents_s3_client.get_contract_file(account.id)
    except Exception as error:
        await context.abort(
            code=StatusCode.INTERNAL,
            details=f"Get contract: {error}"
        )

    return GetContractResponse(contract=build_contract_from_file(file))


async def create_contract(
        context: ServicerContext,
        request: CreateContractRequest,
        documents_s3_client: DocumentsS3Client,
        accounts_grpc_client: AccountsGRPCClient,
) -> CreateContractResponse:
    try:
        account = await accounts_grpc_client.get_account(request.account_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create contract: {error.details()}"
        )

    file = await documents_s3_client.upload_contract_file(account.id, request.content)

    return CreateContractResponse(contract=build_contract_from_file(file))
