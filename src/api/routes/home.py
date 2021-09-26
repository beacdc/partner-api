from fastapi import APIRouter, Request

from api.models.home import HomeResponse
from api.vars import SERVICE_NAME, APP_ENV

router = APIRouter()
tag = "home"


@router.get(
    "/",
    status_code=200,
    tags=[tag],
    description="Give some information about the running service",
)
async def home(req: Request) -> HomeResponse:
    return HomeResponse(service=SERVICE_NAME, environment=APP_ENV)
