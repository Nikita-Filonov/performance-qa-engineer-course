from fastapi import FastAPI

from config import settings
from libs.http.server.base import build_http_server
from services.mock.apps.accounts.http import accounts_mock_router
from services.mock.apps.cards.http import cards_mock_router
from services.mock.apps.documents.contracts.http import contracts_mock_router
from services.mock.apps.documents.receipts.http import receipts_mock_router
from services.mock.apps.documents.tariffs.http import tariffs_mock_router
from services.mock.apps.operations.http import operations_mock_router
from services.mock.apps.users.http import users_mock_router

app = FastAPI(title="mock-service")

app.include_router(users_mock_router)
app.include_router(cards_mock_router)
app.include_router(tariffs_mock_router)
app.include_router(receipts_mock_router)
app.include_router(accounts_mock_router)
app.include_router(contracts_mock_router)
app.include_router(operations_mock_router)

if __name__ == "__main__":
    build_http_server("services.mock.server.http:app", settings.mock_http_server)
