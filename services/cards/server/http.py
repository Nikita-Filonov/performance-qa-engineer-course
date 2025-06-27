from fastapi import FastAPI

from config import settings
from libs.http.server.base import build_http_server
from services.cards.apps.cards.api.cards.http import cards_router

app = FastAPI(title="cards-service")

app.include_router(cards_router)

if __name__ == "__main__":
    build_http_server("services.cards.server.http:app", settings.cards_http_server)
