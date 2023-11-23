from fastapi import FastAPI

from decouple import config

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = config("BOT_TOKEN")
WEBHOOK_PATH = f"/{TOKEN}/"
WEBHOOK_URL = config("WEBHOOK_URL") + WEBHOOK_PATH

app = FastAPI(title="Kelishamiz admin bot")
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
