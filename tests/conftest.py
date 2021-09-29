import asyncio
import sys
from pathlib import Path

import mongomock
import pytest

root = Path.cwd()
sys.path.insert(1, str(root / "src"))

from api.models.partner import Partner, GeoJSON


@pytest.fixture(scope="class")
def scope():
    return {"method": "GET", "type": "http", "headers": None}


@pytest.fixture
def fake_db():
    client = mongomock.MongoClient()
    db = client.db
    return db


@pytest.fixture()
def fake_partner_1():
    coverage_area = GeoJSON(
        type="MultiPolygon",
        coordinates=[
            [
                [
                    [-46.652326583862305, -23.568078093330698],
                    [-46.655030250549316, -23.569297490904663],
                    [-46.65337800979614, -23.57138224117761],
                    [-46.6514253616333, -23.57356529325444],
                    [-46.6495156288147, -23.57307361802522],
                    [-46.64700508117676, -23.570044858015393],
                    [-46.649086475372314, -23.568648458121316],
                    [-46.652326583862305, -23.568078093330698],
                ]
            ],
            [
                [
                    [-46.65290594100952, -23.56475419407091],
                    [-46.651811599731445, -23.56711436788398],
                    [-46.64867877960205, -23.56811742891301],
                    [-46.64623260498047, -23.567252043380726],
                    [-46.64515972137451, -23.56420348074616],
                    [-46.651833057403564, -23.56408547044763],
                    [-46.65290594100952, -23.56475419407091],
                ]
            ],
        ],
    )
    address = GeoJSON(
        type="Point", coordinates=[-46.652798652648926, -23.569297490904663]
    )
    partner_obj = Partner(
        tradingName="Ze do Bela vista - 1",
        ownerName="Juliana Lima",
        document="68648804000135",
        coverageArea=coverage_area,
        address=address,
    )
    return partner_obj


@pytest.fixture()
def fake_partner_2():
    coverage_area = GeoJSON(
        type="MultiPolygon",
        coordinates=[
            [
                [
                    [-46.63440942764282, -23.558007796770593],
                    [-46.64419412612915, -23.558676551328382],
                    [-46.64715528488159, -23.562728344395214],
                    [-46.6453742980957, -23.567468390298316],
                    [-46.63149118423461, -23.566937356319002],
                    [-46.631855964660645, -23.557575071419585],
                    [-46.63440942764282, -23.557830772935592],
                    [-46.63440942764282, -23.558007796770593],
                ]
            ]
        ],
    )
    address = GeoJSON(
        type="Point", coordinates=[-46.64138317108154, -23.56058445003704]
    )
    partner_obj = Partner(
        tradingName="Ze do Bela vista - 2",
        ownerName="Paulo de Marques",
        document="92199532000118",
        coverageArea=coverage_area,
        address=address,
    )
    return partner_obj


@pytest.fixture()
def fake_partner_3():
    coverage_area = GeoJSON(
        type="MultiPolygon",
        coordinates=[
            [
                [
                    [-46.63576126098632, -23.565245900445678],
                    [-46.645116806030266, -23.560525443275637],
                    [-46.660737991333, -23.557535732680662],
                    [-46.65550231933594, -23.572640942300637],
                    [-46.64425849914551, -23.576416973278228],
                    [-46.63576126098632, -23.565245900445678],
                ]
            ]
        ],
    )
    address = GeoJSON(
        type="Point", coordinates=[-46.648828983306885, -23.56750772606323]
    )
    partner_obj = Partner(
        tradingName="Ze do Bela vista - 3",
        ownerName="Otro da Silva",
        document="36114640000170",
        coverageArea=coverage_area,
        address=address,
    )
    return partner_obj


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f
