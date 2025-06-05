from logging import Logger

from httpx import Request, Response


class HTTPLoggerEventHook:
    def __init__(self, logger: Logger):
        self.logger = logger

    async def log_request(self, request: Request):
        self.logger.info(f"{request.method} {request.url} - Waiting for response")

    async def log_response(self, response: Response):
        request = response.request
        self.logger.info(f"{request.method} {request.url} - Status {response.status_code}")
