from fastapi import APIRouter, Request, Response

router = APIRouter()
tag = "health"


@router.get(
    "/health_check",
    status_code=200,
    tags=[tag],
    description="Check if service is alive",
)
async def health_check(req: Request) -> Response:
    return Response(status_code=200)
