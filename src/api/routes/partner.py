from typing import Union

from fastapi import APIRouter, Request

from api.adapters.mongo_adapter import MongoAdapter
from api.exceptions.errors import DefaultError
from api.models.partner import Partner
from api.services.partner_service import PartnerService

router = APIRouter()


@router.post(
    "/partner",
    responses={
        400: {"model": DefaultError},
        401: {"model": DefaultError},
        403: {"model": DefaultError},
        410: {"model": DefaultError},
    },
    response_model=Partner,
    status_code=201,
    tags=["Partner"],
)
async def partner_post(req: Request, partner_obj: Partner):
    db = MongoAdapter.db
    partner_service: PartnerService = PartnerService(db=db)

    response = await partner_service.create_partner(partner_obj)

    return response


@router.get(
    "/partner/{partner_id}",
    responses={
        400: {"model": DefaultError},
        401: {"model": DefaultError},
        403: {"model": DefaultError},
        410: {"model": DefaultError},
    },
    response_model=Union[Partner, None],
    status_code=200,
    tags=["Partner"],
)
async def partner_get(req: Request, partner_id):
    db = MongoAdapter.db
    partner_service: PartnerService = PartnerService(db=db)

    response = await partner_service.search_partner(partner_id)

    return response


@router.get(
    "/partner",
    responses={
        400: {"model": DefaultError},
        401: {"model": DefaultError},
        403: {"model": DefaultError},
        410: {"model": DefaultError},
    },
    response_model=Union[Partner, None],
    status_code=200,
    tags=["Partner"],
)
async def partner_get_nearest(req: Request, lat: float, long: float):
    db = MongoAdapter.db
    partner_service: PartnerService = PartnerService(db=db)

    response = await partner_service.find_nearest_partner(lat=lat, long=long)

    return response
