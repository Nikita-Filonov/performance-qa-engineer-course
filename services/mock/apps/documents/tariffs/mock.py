from pathlib import Path

from libs.logger import get_logger
from libs.mock.loader import MockLoader

loader = MockLoader(
    root=Path("./services/mock/data/documents/tariffs"),
    logger=get_logger("DOCUMENTS_TARIFFS_SERVICE_MOCK_LOADER")
)
