from fastapi import FastAPI

from config import settings
from libs.http.server.base import build_http_server
from services.gateway.apps.accounts.api.accounts.http import accounts_gateway_router
from services.gateway.apps.cards.api.cards.http import cards_gateway_router
from services.gateway.apps.documents.api.documents.http import documents_gateway_router
from services.gateway.apps.operations.api.operations.http import operations_gateway_router
from services.gateway.apps.users.api.users.http import users_gateway_router

app = FastAPI(title="gateway-service")

app.include_router(users_gateway_router)
app.include_router(cards_gateway_router)
app.include_router(accounts_gateway_router)
app.include_router(documents_gateway_router)
app.include_router(operations_gateway_router)

if __name__ == "__main__":
    build_http_server(app, settings.gateway_http_server)
