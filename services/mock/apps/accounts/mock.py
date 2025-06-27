from pathlib import Path

from libs.logger import get_logger
from libs.mock.loader import MockLoader

loader = MockLoader(
    root=Path("./services/mock/data/accounts"),
    logger=get_logger("ACCOUNTS_SERVICE_MOCK_LOADER")
)
