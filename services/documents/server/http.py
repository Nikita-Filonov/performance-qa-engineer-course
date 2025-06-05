from fastapi import FastAPI

from config import settings
from libs.http.server.base import build_http_server
from services.documents.apps.contracts.api.contracts.http import contracts_router
from services.documents.apps.tariffs.api.tariffs.http import tariffs_router

app = FastAPI(title="documents-service")

app.include_router(tariffs_router)
app.include_router(contracts_router)

if __name__ == "__main__":
    build_http_server(app, settings.documents_http_server)
