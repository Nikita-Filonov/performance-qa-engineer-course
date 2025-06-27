from pydantic import BaseModel


class KafkaClientConfig(BaseModel):
    port: int = 9092
    host: str

    @property
    def bootstrap_servers(self) -> str:
        return f"{self.host}:{self.port}"
