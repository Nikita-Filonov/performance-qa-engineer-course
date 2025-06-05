from grpc.aio import ServicerContext

from contracts.services.documents.contracts.contracts_service_pb2_grpc import ContractsServiceServicer
from contracts.services.documents.contracts.rpc_create_contract_pb2 import CreateContractRequest, CreateContractResponse
from contracts.services.documents.contracts.rpc_get_contract_pb2 import GetContractRequest, GetContractResponse
from services.accounts.clients.accounts.grpc import get_accounts_grpc_client
from services.documents.apps.contracts.controllers.contracts.grpc import create_contract, get_contract
from services.documents.services.s3.client import get_documents_s3_client


class ContractsService(ContractsServiceServicer):
    async def GetContract(self, request: GetContractRequest, context: ServicerContext) -> GetContractResponse:
        return await get_contract(
            context=context,
            request=request,
            documents_s3_client=get_documents_s3_client(),
            accounts_grpc_client=get_accounts_grpc_client()
        )

    async def CreateContract(self, request: CreateContractRequest, context: ServicerContext) -> CreateContractResponse:
        return await create_contract(
            context=context,
            request=request,
            documents_s3_client=get_documents_s3_client(),
            accounts_grpc_client=get_accounts_grpc_client()
        )
