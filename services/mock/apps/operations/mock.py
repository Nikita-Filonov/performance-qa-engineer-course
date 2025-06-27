from pathlib import Path

from libs.logger import get_logger
from libs.mock.loader import MockLoader

loader = MockLoader(
    root=Path("./services/mock/data/operations"),
    logger=get_logger("OPERATIONS_SERVICE_MOCK_LOADER")
)
