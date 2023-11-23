import datetime

from .db import DB
from loader import TOKEN


class Tokens(DB):

    def __init__(self):
        super().__init__()
        self.col = self.db["tokens"]

    async def insert(self, access_token, refresh_token):
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=2)
        token_data = {
            "access_token": access_token,
            "bot_token": TOKEN,
            "refresh_token": refresh_token,
            "expires_at": expires_at
        }
        result = await self.col.insert_one(token_data)
        token_id = result.inserted_id
        return token_id

    async def read(self, bot_token):
        result = await self.col.find_one({"bot_token": bot_token})
        return result

    async def update(self, bot_token, access_token, refresh_token):
        new_expire = datetime.datetime.now() + datetime.timedelta(hours=2)
        updated_data = {
            "$set": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": new_expire
            }
        }
        await self.col.update_one({"bot_token": bot_token}, updated_data)

    async def delete(self, bot_token):
        await self.col.delete_one({"bot_token": bot_token})
