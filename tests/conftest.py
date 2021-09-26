import asyncio

import mongomock
import pytest

from api.models.partner import Partner, GeoJSON


@pytest.fixture(scope="class")
def scope():
    return {"method": "GET", "type": "http", "headers": None}


@pytest.fixture
def fake_client():
    client = mongomock.MongoClient()
    return client


@pytest.fixture()
def fake_partner():
    coverage_area = GeoJSON(
        type="MultiPolygon",
        coordinates=[
            [[[30, 20], [45, 40], [10, 40], [30, 20]]],
            [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]],
        ],
    )
    address = GeoJSON(type="Point", coordinates=[-46.57421, -21.785741])
    partner_obj = Partner(
        tradingName="Teste do Ze",
        ownerName="Ze do Teste",
        document="1432132123891",
        coverageArea=coverage_area,
        address=address,
    )
    return partner_obj


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f
