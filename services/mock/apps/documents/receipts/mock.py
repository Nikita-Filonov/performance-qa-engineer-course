from pathlib import Path

from libs.logger import get_logger
from libs.mock.loader import MockLoader

loader = MockLoader(
    root=Path("./services/mock/data/documents/receipts"),
    logger=get_logger("DOCUMENTS_RECEIPTS_SERVICE_MOCK_LOADER")
)
