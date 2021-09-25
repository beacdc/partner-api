import pytest
from fastapi import Request

from api.models.home import HomeResponse
from api.routes.home import home
from api.vars import SERVICE_NAME, APP_ENV


@pytest.mark.asyncio
async def test_home_route_response_type(scope):
    req = Request(scope=scope)
    resp = await home(req)
    assert resp == HomeResponse(service=SERVICE_NAME, environment=APP_ENV)
