from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from logging import info
from odmantic import AIOEngine

from motor import motor_asyncio,core
from pymongo.driver_info import DriverInfo
from pymongo import MongoClient

from src.config import get_config

config = get_config()

DRIVER_INFO = DriverInfo(name="full-stack-fastapi-mongodb")


class _MongoClientSingleton:
    mongo_client: Optional[motor_asyncio.AsyncIOMotorClient]
    engine: AIOEngine

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                config.MONGODB_URI, driver=DRIVER_INFO
            )
            cls.instance.engine = AIOEngine(client=cls.instance.mongo_client, database=config.MONGO_DATABASE)
        return cls.instance


def MongoDatabase() -> core.AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[config.MONGO_DATABASE]


# Assíncrona
# def get_engine() -> AIOEngine:
#     return _MongoClientSingleton().engine

# Maneira síncrona
def get_engine():
    return MongoClient(config.MONGODB_URI)['payment']


async def ping():
    await MongoDatabase().command("ping")


__all__ = ["MongoDatabase", "ping"]