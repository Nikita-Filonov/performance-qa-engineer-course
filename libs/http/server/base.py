import uvicorn

from libs.config.http import HTTPServerConfig


def build_http_server(app: str, config: HTTPServerConfig):
    uvicorn.run(app=app, host=str(config.host), port=config.port, workers=3)
