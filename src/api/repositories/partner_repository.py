from typing import List, Union

from pymongo import MongoClient
from pymongo.collection import Collection

from api.models.partner import Partner


class PartnerRepository:
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection: Collection = self.client.db["Partner"]

    async def insert(self, partner: Union[Partner, List[Partner]]):
        result = self.collection.insert_one(partner.dict(exclude_none=True))
        return result.inserted_id

    async def find_by_id(self, partner_id: str) -> dict:
        result = self.collection.find_one({"_id": partner_id})
        return result

    async def find_by_document(self, document: str) -> dict:
        result = self.collection.find_one({"document": document})
        return result

    async def find_within(self, long: float, lat: float) -> dict:
        result = self.collection.find(
            {
                "coverageArea": {
                    "$geoIntersects": {
                        "$geometry": {"type": "Point", "coordinates": [long, lat]}
                    }
                }
            }
        )
        return result
