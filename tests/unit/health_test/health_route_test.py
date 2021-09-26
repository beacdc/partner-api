import pytest
from fastapi import Request, Response
from api.routes.health import health_check


@pytest.mark.asyncio
async def test_health_route_response_type(scope):
    req = Request(scope=scope)
    resp = await health_check(req)
    assert isinstance(resp, Response)


@pytest.mark.asyncio
async def test_health_route_response_code_200(scope):
    req = Request(scope=scope)
    resp = await health_check(req)
    assert resp.status_code == 200
