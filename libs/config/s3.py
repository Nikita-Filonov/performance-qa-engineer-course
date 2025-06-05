from pydantic import BaseModel, HttpUrl


class S3ClientConfig(BaseModel):
    bucket: str
    access_key: str
    secret_key: str
    public_url: HttpUrl
    internal_url: HttpUrl

    def get_file_url(self, key: str) -> str:
        return f"{self.public_url}{self.bucket}/{key}"
