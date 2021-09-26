from enum import Enum
from typing import Optional

from pydantic import BaseModel


class GeoType(str, Enum):
    MultiPolygon = "MultiPolygon"
    Point = "Point"


class GeoJSON(BaseModel):
    type: GeoType
    coordinates: list


class Partner(BaseModel):
    id: Optional[str]
    tradingName: str
    ownerName: str
    document: str
    coverageArea: GeoJSON
    address: GeoJSON
