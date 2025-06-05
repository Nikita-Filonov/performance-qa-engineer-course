from pydantic import BaseModel, IPvAnyAddress, HttpUrl


class HTTPServerConfig(BaseModel):
    port: int
    host: IPvAnyAddress


class HTTPClientConfig(BaseModel):
    host: HttpUrl
    retries: int = 5
    timeout: float = 120.0

    @property
    def url(self) -> str:
        return str(self.host)
