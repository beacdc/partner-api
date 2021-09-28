import json
from datetime import datetime

from fastapi import Request, Response
from starlette.responses import StreamingResponse

from api.logging.logger import Logger


async def process_request(request: Request) -> Request:
    request.state.start_time = datetime.now()
    path_params = request.path_params
    query_params = dict(request.query_params)
    try:
        request_body = await request.json()
    except Exception:
        request_body = {}

    Logger.info(
        message=f"INCOMING REQUEST {request.method.upper()} {request.url.path}",
        payload=request_body,
        path_params=path_params,
        query_params=query_params,
    )

    return request


async def process_response(request: Request, response: StreamingResponse) -> Response:

    took = round(
        (datetime.now() - request.state.start_time).total_seconds() * 1000.0, 2
    )

    # Formatting response body for logging
    resp_body = {}
    try:
        resp_body = [section async for section in response.__dict__["body_iterator"]]
        # Repairing FastAPI response
        response.__setattr__("body_iterator", AsyncWrapper(resp_body))
        resp_body = json.loads(resp_body[0].decode())
    except Exception:
        resp_body = str(resp_body)
    Logger.info(
        message=f"OUTGOING RESPONSE {request.method.upper()} {request.url.path} {response.status_code} took {took} ms",
        payload=resp_body,
    )

    return response


class AsyncWrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
