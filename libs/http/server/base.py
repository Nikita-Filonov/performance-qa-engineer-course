import uvicorn
from fastapi import FastAPI

from libs.config.http import HTTPServerConfig


def build_http_server(app: FastAPI, config: HTTPServerConfig):
    uvicorn.run(app=app, host=str(config.host), port=config.port)
