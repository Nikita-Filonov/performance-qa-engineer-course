from pydantic import BaseModel, SecretStr


class RedisClientConfig(BaseModel):
    port: int = 6379
    host: str
    password: SecretStr
