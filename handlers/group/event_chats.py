from datetime import datetime

from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold

from decouple import config

from loader import bot
from keyboards.inline.group import approve_or_reject

router = Router()
headers = {'Accept': 'application/json'}
host_url = config("HOST_URL")
group_id = config("GROUP_ID")


async def send_chat_data(
    classified_id: int,
    title: str,
    category: str,
    currency_type: str,
    price: float,
    status: str,
    description: str,
    dynamic_fields: list | None,
    images: list | None,
    location: str,
    created_at: datetime,
    chat_id: int = group_id
) -> None:
    if currency_type == "usd":
        price = f"${price}"
    else:
        price = f"{price} so'm"

    result_dynamic_fields = ""
    if dynamic_fields:
        for dynamic_field in dynamic_fields:
            result_dynamic_fields += f"\n{dynamic_field['key']}: {dynamic_field['value']}"

    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    formatted = created_at.strftime("%Y.%m.%d, %H:%M")
    text = f"Sarlavha: {title}\nKategoriya: {category}\nStatus: {hbold(status).upper()}\nNarxi: {price}\nTavsifi: {description}\nManzil: {location}\nYaratilgan vaqt: {formatted}"

    if result_dynamic_fields:
        text += result_dynamic_fields

    media = []

    for image in images:
        media.append(types.InputMediaPhoto(
            media=image['imageUrl']
        ))

    markup = approve_or_reject(classified_id)

    await bot.send_media_group(
        chat_id=chat_id,
        media=media
    )
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=markup,
        parse_mode=ParseMode.HTML
    )
