import motor.motor_asyncio

from decouple import config

db_username = config("DB_USERNAME")
db_password = config("DB_PASSWORD")

mongo_host = f"mongodb+srv://{db_username}:{db_password}@cluster0.atrk1sf.mongodb.net/?retryWrites=true&w=majority"


class DB:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_host)
        self.db = self.client["kelishamiz-bot"]
