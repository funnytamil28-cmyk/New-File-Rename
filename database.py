from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user_settings

    async def set_user_data(self, user_id, key, value):
        await self.col.update_one(
            {"_id": user_id},
            {"$set": {key: value}},
            upsert=True
        )

    async def get_user_data(self, user_id):
        user = await self.col.find_one({"_id": user_id})
        return user if user else {}

db = Database(Config.MONGO_URL, Config.DB_NAME)
