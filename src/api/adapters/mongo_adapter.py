import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from api.vars import DB_USER, DB_PASSWORD, DB_CLUSTER, DB_NAME, DB_HOST


class MongoAdapter:
    path = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}.{DB_HOST}/{DB_NAME}?retryWrites=true&w=majority"
    client: MongoClient
    db: Database

    @classmethod
    def create_engine(cls):
        cls.client = pymongo.MongoClient(cls.path)
        cls.db = cls.client[DB_NAME]
