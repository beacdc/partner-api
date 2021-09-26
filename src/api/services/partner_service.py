from pymongo import MongoClient

from api.domains.partner_domain import partner_to_dict
from api.exceptions.errors import PartnerNotFound, NearestNotFound
from api.models.partner import Partner
from api.repositories.partner_repository import PartnerRepository


class PartnerService:
    def __init__(self, client: MongoClient) -> None:
        self.repository = PartnerRepository(client=client)

    async def create_partner(self, partner: Partner) -> dict:
        insert_id = await self.repository.insert(partner)
        partner.id = insert_id
        return partner.dict()

    async def search_partner(self, partner_id: str) -> dict:
        partner = await self.repository.find_by_id(partner_id)
        if not partner:
            raise PartnerNotFound(id=partner_id)
        return partner_to_dict(partner)

    async def find_nearest_partner(self, long: float, lat: float):
        partners = await self.repository.find_within(long=long, lat=lat)
        if not partners:
            raise NearestNotFound(long=long, lat=lat)
