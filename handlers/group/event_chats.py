import aiohttp
from datetime import datetime

from aiogram.types import Message
from aiogram import Router, types, F
from aiogram.utils.markdown import hbold

from decouple import config

from keyboards.inline.group import approve_or_reject

router = Router()
headers = {'Accept': 'application/json'}
host_url = config("HOST_URL")
CHATS = list(map(int, config("ADMINS").split(",")))


@router.message()
async def send_chat_data(
    title: str,
    category: str,
    currency_type: str,
    price: float,
    description: str,
    dynamic_fields: list | None,
    location: str,
    created_at: datetime
) -> None:
    if currency_type == "usd":
        price = f"${price}"
    else:
        price = f"{price} so'm"

    result_dynamic_fields = ""
    if dynamic_fields:
        for dynamic_field in dynamic_fields:
            result_dynamic_fields += f"{dynamic_field['key']}: {dynamic_field['value']}\n"

    text = f"{title}\n{category}\n{price}\n{description}\n{location}\n{created_at}"

    if result_dynamic_fields:
        text += result_dynamic_fields

    markup = approve_or_reject()
