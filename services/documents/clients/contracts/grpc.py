from config import settings
from contracts.services.documents.contracts.contract_pb2 import Contract
from contracts.services.documents.contracts.contracts_service_pb2_grpc import ContractsServiceStub
from contracts.services.documents.contracts.rpc_create_contract_pb2 import CreateContractRequest, CreateContractResponse
from contracts.services.documents.contracts.rpc_get_contract_pb2 import GetContractRequest, GetContractResponse
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger


class ContractsGRPCClient(GRPCClient):
    stub: ContractsServiceStub
    stub_class = ContractsServiceStub

    async def get_contract_api(self, request: GetContractRequest) -> GetContractResponse:
        return await self.stub.GetContract(request)

    async def create_contract_api(self, request: CreateContractRequest) -> CreateContractResponse:
        return await self.stub.CreateContract(request)

    async def get_contract(self, account_id: str) -> Contract:
        request = GetContractRequest(account_id=account_id)
        response = await self.get_contract_api(request)
        return response.contract

    async def create_contract(self, account_id: str, content: bytes) -> Contract:
        request = CreateContractRequest(account_id=account_id, content=content)
        response = await self.create_contract_api(request)
        return response.contract


def get_contracts_grpc_client() -> ContractsGRPCClient:
    logger = get_logger("CONTRACTS_SERVICE_GRPC_CLIENT")
    return ContractsGRPCClient(config=settings.documents_grpc_client, logger=logger)
