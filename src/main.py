import asyncio
from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from api.adapters.mongo_adapter import MongoAdapter
from api.exceptions.errors import format_traceback, DefaultError
from api.middlewares.request_timing import process_request, process_response
from api.routes.router import routes
from api.logging.logger import Logger
from fastapi.openapi.utils import get_openapi
from api.vars import PORT, HOST, SERVICE_NAME, VERSION

loop = asyncio.get_event_loop()


async def on_startup():
    Logger.start_logger()
    Logger.info(f"Service {SERVICE_NAME} starting...",)
    connection = MongoAdapter()
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

    @api.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exception: Exception):
        Logger.critical(message=format_traceback())
        msg = DefaultError.default()
        msg.traceback = str(exception)
        return JSONResponse(status_code=500, content=msg.dict(exclude_none=True))

    @api.middleware("http")
    async def request_timing_middleware(request: Request, call_next):
        request = await process_request(request)
        response = await call_next(request)
        response = await process_response(request, response)
        return response

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
