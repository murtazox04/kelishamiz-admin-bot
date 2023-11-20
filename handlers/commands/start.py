import aiohttp

from aiogram.filters import CommandStart
from aiogram import Router, types, F

from decouple import config

router = Router()
headers = {'Accept': 'application/json'}
host_url = config("HOST_URL")
ADMINS = list(map(int, config("ADMINS").split(",")))


@router.message(CommandStart(), F.chat.id.in_(ADMINS))
async def start(message: types.Message) -> None:
    text = f"Assalomu alaykum!\nAdmin botga xush kelibsiz!!!"

    await message.answer(text)
