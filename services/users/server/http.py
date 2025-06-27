from fastapi import FastAPI

from config import settings
from libs.http.server.base import build_http_server
from services.users.apps.users.api.users.http import users_router

app = FastAPI(title="users-service")

app.include_router(users_router)

if __name__ == "__main__":
    build_http_server("services.users.server.http:app", settings.users_http_server)
