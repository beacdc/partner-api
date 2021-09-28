import asyncio

from fastapi import FastAPI

from api.adapters.mongo_adapter import MongoConnector
from api.routes.router import routes
from api.logging.logger import Logger
from fastapi.openapi.utils import get_openapi
from api.vars import PORT, HOST, SERVICE_NAME, VERSION

loop = asyncio.get_event_loop()


async def on_startup():
    Logger.start_logger()
    Logger.info(f"Service {SERVICE_NAME} starting...",)
    connection = MongoConnector()
    connection.create_engine()


async def on_shutdown():
    Logger.info(f"Service {SERVICE_NAME} shutting down...",)


def create() -> FastAPI:
    api = FastAPI(
        title=f"{SERVICE_NAME}",
        description="FastAPI Base API v0.0.1",
        version=f"{VERSION}",
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )

    for route in routes:
        api.include_router(route)

    api.openapi_schema = get_openapi(
        title=f"{SERVICE_NAME}",
        description="FastAPI Base API v0.0.1",
        version=api.version,
        routes=api.routes,
    )

    return api


app = application = create()

if __name__ == "__main__":
    from uvicorn import run

    host = HOST
    port = int(PORT)
    run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        use_colors=True,
        log_level="WARNING".lower(),
    )
