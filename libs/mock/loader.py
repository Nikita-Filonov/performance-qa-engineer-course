import asyncio
import random
from logging import Logger
from pathlib import Path
from typing import TypeVar, Type, Literal

import aiofiles
from google.protobuf.json_format import Parse
from google.protobuf.message import Message
from pydantic import BaseModel

# Типы для HTTP и GRPC моделей
HTTPModelT = TypeVar("HTTPModelT", bound=BaseModel)
GRPCModelT = TypeVar("GRPCModelT", bound=Message)


class MockLoader:
    """
    Класс для загрузки мок-данных (HTTP и gRPC) из файловой системы.

    Позволяет загружать и валидировать данные в формате JSON
    для HTTP (через Pydantic) и gRPC (через protobuf).
    """

    def __init__(self, root: Path, logger: Logger):
        """
        :param root: Корневая директория с моками, например: Path("./services/mock/data/accounts")
        :param logger: Инстанс логгера для логирования операций загрузки
        """
        self.root = root
        self.logger = logger

    async def get_raw_data(self, protocol: Literal['http', 'grpc'], file: str) -> str:
        """
        Получает необработанные данные из файла мока по указанному протоколу.

        :param protocol: Протокол ('http' или 'grpc')
        :param file: Относительный путь к файлу (например, "get_account/default.json")
        :return: Содержимое файла как строка
        :raises FileNotFoundError: если файл не найден
        """
        mock_file = self.root / protocol / file

        if not mock_file.exists():
            self.logger.error(f"Mock file not found: {mock_file}")
            raise FileNotFoundError(f"Mock file not found: {mock_file}")

        self.logger.info(f"Loading mock file: {mock_file}")
        async with aiofiles.open(mock_file, mode='r', encoding='utf-8') as async_file:
            return await async_file.read()

    async def load_http(self, file: str, model: Type[HTTPModelT]) -> HTTPModelT:
        """
        Загружает HTTP мок-файл и валидирует его через указанную Pydantic-модель.

        :param file: Путь к файлу мока (например, "get_account/default.json")
        :param model: Класс Pydantic-модели для валидации
        :return: Экземпляр модели с валидированными данными
        """
        raw = await self.get_raw_data("http", file)
        self.logger.debug(f"Validating HTTP mock with Pydantic model: {model.__name__}")
        return model.model_validate_json(raw)

    async def load_grpc(self, file: str, model: Type[GRPCModelT]) -> GRPCModelT:
        """
        Загружает gRPC мок-файл и парсит его в protobuf-сообщение.

        :param file: Путь к файлу мока (например, "get_account/default.json")
        :param model: Класс protobuf-сообщения
        :return: Экземпляр protobuf-сообщения с распарсенными данными
        """
        raw = await self.get_raw_data("grpc", file)
        self.logger.debug(f"Validating gRPC mock with Protobuf message: {model.__name__}")
        return Parse(raw, model())

    async def load_http_with_timeout(self, file: str, model: Type[HTTPModelT]) -> HTTPModelT:
        """
        Загружает HTTP мок с искусственной задержкой для имитации сетевой задержки.
        """
        await asyncio.sleep(random.uniform(0.05, 0.1))
        return await self.load_http(file, model)

    async def load_grpc_with_timeout(self, file: str, model: Type[GRPCModelT]) -> GRPCModelT:
        """
        Загружает gRPC мок с искусственной задержкой для имитации сетевой задержки.
        """
        await asyncio.sleep(random.uniform(0.05, 0.1))
        return await self.load_grpc(file, model)
