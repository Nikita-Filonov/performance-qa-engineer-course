from pydantic import BaseModel, SecretStr


class PostgresConfig(BaseModel):
    port: int = 5432
    host: str
    driver: str
    database: str
    username: str
    password: SecretStr

    @property
    def url(self) -> str:
        return (
            f"{self.driver}://{self.username}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.database}"
        )
