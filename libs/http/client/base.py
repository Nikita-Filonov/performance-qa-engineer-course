from logging import Logger
from typing import Any, Optional

from fastapi import status
from httpx import AsyncClient, Response, Timeout, Headers, URL, QueryParams

from libs.config.http import HTTPClientConfig
from libs.http.client.event_hooks.logger_event_hook import HTTPLoggerEventHook

URLType = URL | str


class HTTPClient:
    retry_statuses: list[int] = [
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        status.HTTP_503_SERVICE_UNAVAILABLE,
        status.HTTP_504_GATEWAY_TIMEOUT
    ]

    def __init__(
            self,
            config: HTTPClientConfig,
            logger: Logger,
            headers: Optional[Headers] = None
    ) -> None:
        logger_event_hook = HTTPLoggerEventHook(logger=logger)

        self.client = AsyncClient(
            base_url=config.url,
            timeout=Timeout(timeout=config.timeout),
            headers=headers,
            event_hooks={
                'request': [logger_event_hook.log_request],
                'response': [logger_event_hook.log_response]
            }
        )
        self.logger = logger
        self.config = config
        self.headers = headers

    async def send_with_retries(
            self,
            method: str,
            url: URLType,
            json: Optional[Any] = None,
            params: Optional[QueryParams] = None,
            headers: Optional[Headers] = None
    ) -> Response:
        response: Response | None = None

        attempt = 0
        while attempt < self.config.retries:
            response = await self.client.request(
                method,
                url=url,
                json=json,
                params=params,
                headers=headers
            )
            status_code = response.status_code

            if status_code not in self.retry_statuses:
                return response

            self.logger.error(
                f'{method} {response.request.url} - Unexpected status {status_code}, retrying'
            )

            attempt += 1

        return response

    async def get(
            self,
            url: URLType,
            params: Optional[QueryParams] = None,
            headers: Optional[Headers] = None
    ) -> Response:
        return await self.send_with_retries(
            "GET",
            url=url,
            params=params,
            headers=headers
        )

    async def post(self, url: URLType, json: Optional[Any] = None) -> Response:
        return await self.send_with_retries("POST", url=url, json=json)
