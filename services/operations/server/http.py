from fastapi import FastAPI

from config import settings
from libs.http.server.base import build_http_server
from services.operations.apps.operations.api.operations.http import operations_router

app = FastAPI(title="operations-service")

app.include_router(operations_router)

if __name__ == "__main__":
    build_http_server(app, settings.operations_http_server)
