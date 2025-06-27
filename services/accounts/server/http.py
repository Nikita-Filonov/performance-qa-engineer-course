from fastapi import FastAPI

from config import settings
from libs.http.server.base import build_http_server
from services.accounts.apps.accounts.api.accounts.http import accounts_router

app = FastAPI(title="accounts-service")

app.include_router(accounts_router)

if __name__ == "__main__":
    build_http_server("services.accounts.server.http:app", settings.accounts_http_server)
