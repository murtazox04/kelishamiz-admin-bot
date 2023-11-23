import aiohttp

from decouple import config
from datetime import datetime

from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.utils.markdown import hbold

from loader import bot
from callbacks import CheckStatus
from handlers.utils import get_access_token
from keyboards.inline.group import delete_classified

router = Router()
host_url = config("HOST_URL")
ADMINS = list(map(int, config("ADMINS").split(",")))
chat_id = config('CHANNEL_ID')


@router.callback_query(CheckStatus.filter(F.status == "approve"), F.chat.id.in_(ADMINS))
async def approve_classified(callback_data: CheckStatus) -> None:
    classified_id = callback_data.classified_id
    json_data = {"status": "approved"}

    access_token = await get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = host_url + f"/admin/classifieds/{classified_id}/"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url, json=json_data) as response:
            data = await response.json()

            classified_id = data['id']
            title = data['title']
            category = data['category']
            currency_type = data['detail']['currencyType']
            status = data['status']
            price = data['detail']['price']
            images = data['detail']['images']
            description = data['detail']['description']
            dynamic_fields = data['detail']['dynamicFields']
            location = data['detail']['location']
            created_at = data['createdAt']

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
            images[0].caption = text
            images[0].parse_mode = ParseMode.HTML

            await bot.send_media_group(
                chat_id=chat_id,
                media=media
            )


@router.callback_query(CheckStatus.filter(F.status == "reject"), F.chat.id.in_(ADMINS))
async def reject_classified(callback_query: types.CallbackQuery, callback_data: CheckStatus) -> None:
    classified_id = callback_data.classified_id
    json_data = {"status": "rejected"}

    access_token = await get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = host_url + f"/admin/classifieds/{classified_id}/"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url, json=json_data) as response:
            data = await response.json()

            classified_id = data['id']
            title = data['title']
            category = data['category']
            currency_type = data['detail']['currencyType']
            status = data['status']
            price = data['detail']['price']
            description = data['detail']['description']
            dynamic_fields = data['detail']['dynamicFields']
            location = data['detail']['location']
            created_at = data['createdAt']

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

            markup = delete_classified(classified_id)

            await callback_query.message.edit_text(
                text=text,
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN
            )


@router.callback_query(CheckStatus.filter(F.status == "delete"), F.chat.id.in_(ADMINS))
async def reject_classified(callback_query: types.CallbackQuery, callback_data: CheckStatus) -> None:
    classified_id = callback_data.classified_id
    json_data = {"status": "deleted"}

    access_token = await get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = host_url + f"/admin/classifieds/{classified_id}/"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url, json=json_data) as response:
            data = await response.json()

            classified_id = data['id']
            title = data['title']
            category = data['category']
            currency_type = data['detail']['currencyType']
            status = data['status']
            price = data['detail']['price']
            description = data['detail']['description']
            dynamic_fields = data['detail']['dynamicFields']
            location = data['detail']['location']
            created_at = data['createdAt']

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

            await callback_query.message.edit_text(
                text=text,
                reply_markup=None,
                parse_mode=ParseMode.MARKDOWN
            )
