from pydantic import BaseModel, IPvAnyAddress


class GRPCServerConfig(BaseModel):
    port: int
    host: IPvAnyAddress

    @property
    def url(self):
        return f'{self.host}:{self.port}'


class GRPCClientConfig(BaseModel):
    port: int
    host: str
    retries: int = 10
    timeout: float = 180.0
    insecure_skip_verify: bool = True

    @property
    def url(self):
        return f'{self.host}:{self.port}'
