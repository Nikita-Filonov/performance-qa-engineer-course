import json
from logging import Logger
from typing import Any

from redis.asyncio import Redis
from redis.typing import EncodableT, KeyT

from libs.config.redis import RedisClientConfig


class RedisClient:
    def __init__(self, prefix: str, config: RedisClientConfig, logger: Logger):
        self.prefix = prefix
        self.client = Redis(
            host=config.host,
            port=config.port,
            password=config.password.get_secret_value(),
            username=None,
            decode_responses=True,
        )
        self.logger = logger

    def full_key(self, key: str) -> str:
        return f'{self.prefix}.{key}'

    async def set(self, key: KeyT, value: EncodableT, expire: int = 3600) -> None:
        full_key = self.full_key(key)
        try:
            await self.client.set(full_key, value, ex=expire)
            self.logger.info(f"Set key '{full_key}' with expiration {expire}s")
        except Exception as error:
            self.logger.exception(f"Failed to set key '{full_key}': {error}")

    async def get(self, key: KeyT) -> str | None:
        full_key = self.full_key(key)
        try:
            value = await self.client.get(f'{self.prefix}.{key}')
            self.logger.info(f"Fetched key '{full_key}': {value}")
            return value
        except Exception as error:
            self.logger.exception(f"Failed to get key '{full_key}': {error}")
            return None

    async def get_json(self, key: KeyT) -> Any | None:
        raw_value = await self.get(key)
        if raw_value is None:
            self.logger.debug(f"No value found for key '{self.full_key(key)}'")
            return None

        try:
            data = json.loads(raw_value)
            self.logger.debug(f"Deserialized JSON for key '{self.full_key(key)}': {data}")
            return data
        except json.JSONDecodeError as error:
            self.logger.exception(f"Failed to decode JSON for key '{self.full_key(key)}': {error}")
            return None

    async def set_json(self, key: KeyT, value: Any, expire: int = 3600) -> None:
        try:
            json_data = json.dumps(value)
            await self.set(key, json_data, expire)
            self.logger.debug(f"Stored JSON for key '{self.full_key(key)}'")
        except (TypeError, ValueError) as error:
            self.logger.exception(
                f"Failed to serialize value to JSON for key '{self.full_key(key)}': {error}"
            )
