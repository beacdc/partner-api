from pymongo.database import Database

from api.domains.partner_domain import partner_to_dict, validate_and_format_document
from api.exceptions.errors import (
    PartnerNotFound,
    NearestNotFound,
    InvalidDocumentNumber,
    DuplicateDocumentNumber,
)
from api.models.partner import Partner
from api.repositories.partner_repository import PartnerRepository


class PartnerService:
    def __init__(self, db: Database) -> None:
        self.repository = PartnerRepository(db=db)

    async def create_partner(self, partner: Partner) -> dict:
        partner.document, is_valid = await validate_and_format_document(
            partner.document
        )
        if not is_valid:
            raise InvalidDocumentNumber(document=partner.document)
        duplicate_partner = await self.repository.find_by_document(partner.document)
        if duplicate_partner:
            raise DuplicateDocumentNumber(document=partner.document)
        insert_id = await self.repository.insert(partner)
        partner.id = str(insert_id)
        return partner.dict()

    async def search_partner(self, partner_id: str) -> dict:
        partner = await self.repository.find_by_id(partner_id)
        if not partner:
            raise PartnerNotFound(id=partner_id)
        return await partner_to_dict(partner)

    async def find_nearest_partner(self, long: float, lat: float):
        partner = await self.repository.find_within(long=long, lat=lat)
        if not partner:
            raise NearestNotFound(long=long, lat=lat)
        return await partner_to_dict(partner)
