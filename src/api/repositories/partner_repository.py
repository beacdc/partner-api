from typing import List, Union

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database

from api.models.partner import Partner


class PartnerRepository:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.collection: Collection = self.db["Partner"]

    async def insert(self, partner: Union[Partner, List[Partner]]):
        result = self.collection.insert_one(partner.dict(exclude_none=True))
        return result.inserted_id

    async def find_by_id(self, partner_id: str) -> dict:
        result = self.collection.find_one({"_id": ObjectId(partner_id)})
        return result

    async def find_by_document(self, document: str) -> dict:
        result = self.collection.find_one({"document": document})
        return result

    async def find_within(self, long: float, lat: float) -> dict:
        result = self.collection.find_one(
            {
                "$and": [
                    {
                        "coverageArea": {
                            "$geoIntersects": {
                                "$geometry": {
                                    "type": "Point",
                                    "coordinates": [long, lat],
                                }
                            }
                        }
                    },
                    {
                        "coverageArea": {
                            "$near": {
                                "$geometry": {
                                    "type": "Point",
                                    "coordinates": [long, lat],
                                }
                            }
                        }
                    },
                ]
            }
        )
        return result
