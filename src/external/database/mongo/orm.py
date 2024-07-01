import os
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import get_config

config = get_config()

CONNECTION_STRING = config.MONGODB_URI

engine = AsyncIOMotorClient(CONNECTION_STRING)
# engine = create_engine(config.DATABASE_URL, echo=True)

# if __name__ == '__main__':
    # print(engine)


