from grpc.aio import ServicerContext

from contracts.services.documents.contracts.contracts_service_pb2_grpc import ContractsServiceServicer
from contracts.services.documents.contracts.rpc_create_contract_pb2 import CreateContractRequest, CreateContractResponse
from contracts.services.documents.contracts.rpc_get_contract_pb2 import GetContractRequest, GetContractResponse
from services.mock.apps.documents.contracts.mock import loader


class ContractsMockService(ContractsServiceServicer):
    async def GetContract(self, request: GetContractRequest, context: ServicerContext) -> GetContractResponse:
        return loader.load_grpc("GetContract/default.json", GetContractResponse)

    async def CreateContract(self, request: CreateContractRequest, context: ServicerContext) -> CreateContractResponse:
        return loader.load_grpc("CreateContract/default.json", CreateContractResponse)
