from enum import Enum

from pydantic import BaseModel


class EnvNames(str, Enum):
    local = "LOCAL"
    development = "DEV"
    test = "TEST"
    production = "LIVE"
    staging = "STAGING"
    sandbox = "SANDBOX"


class HomeResponse(BaseModel):
    service: str
    environment: EnvNames
