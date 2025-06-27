from pathlib import Path

from libs.logger import get_logger
from libs.mock.loader import MockLoader

loader = MockLoader(
    root=Path("./services/mock/data/users"),
    logger=get_logger("USERS_SERVICE_MOCK_LOADER")
)
