from grpc.aio import AioRpcError, ServicerContext

from contracts.services.documents.tariffs.rpc_create_tariff_pb2 import CreateTariffRequest, CreateTariffResponse
from contracts.services.documents.tariffs.rpc_get_tariff_pb2 import GetTariffRequest, GetTariffResponse
from contracts.services.documents.tariffs.tariff_pb2 import Tariff
from libs.s3.client import S3File
from services.accounts.clients.accounts.grpc import AccountsGRPCClient
from services.documents.services.s3.client import DocumentsS3Client


def build_tariff_from_file(file: S3File) -> Tariff:
    return Tariff(url=file.url, document=file.content)


async def get_tariff(
        context: ServicerContext,
        request: GetTariffRequest,
        documents_s3_client: DocumentsS3Client,
        accounts_grpc_client: AccountsGRPCClient,
) -> GetTariffResponse:
    try:
        account = await accounts_grpc_client.get_account(request.account_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Get tariff: {error.details()}"
        )

    file = await documents_s3_client.get_tariff_file(account.id)

    return GetTariffResponse(tariff=build_tariff_from_file(file))


async def create_tariff(
        context: ServicerContext,
        request: CreateTariffRequest,
        documents_s3_client: DocumentsS3Client,
        accounts_grpc_client: AccountsGRPCClient,
) -> CreateTariffResponse:
    try:
        account = await accounts_grpc_client.get_account(request.account_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create tariff: {error.details()}"
        )

    file = await documents_s3_client.upload_tariff_file(account.id, request.content)

    return GetTariffResponse(tariff=build_tariff_from_file(file))
