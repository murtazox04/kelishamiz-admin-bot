import aiohttp

from aiogram.enums import ParseMode
from aiogram import Router, types, F
from aiogram.utils.markdown import hbold, hcode

from decouple import config

from callbacks import CheckStatus
from handlers.utils import get_access_token
from keyboards.inline.group import delete_classified
from handlers.group.event_chats import send_chat_data

router = Router()
host_url = config("HOST_URL")
ADMINS = list(map(int, config("ADMINS").split(",")))
chat_id = config('CHANNEL_ID')


@router.callback_query(CheckStatus.filter(F.status == "approve"))
async def approve_classified(callback_query: types.CallbackQuery, callback_data: CheckStatus):
    classified_id = callback_data.classified_id
    data = {"status": "approved"}

    access_token = await get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = host_url + f"/admin/classifieds/{classified_id}/"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url, json=data) as response:
            data = await response.json()
            await send_chat_data(
                classified_id=data['id'],
                title=data['title'],
                category=data['category'],
                currency_type=data['detail']['currencyType'],
                price=data['detail']['price'],
                description=data['detail']['description'],
                dynamic_fields=data['detail']['dynamicFields'],
                location=data['detail']['location'],
                images=data['detail']['images'],
                created_at=data['createdAt'],
                chat_id=chat_id
            )


@router.callback_query(CheckStatus.filter(F.status == "reject"))
async def reject_classified(callback_query: types.CallbackQuery, callback_data: CheckStatus) -> None:
    classified_id = callback_data.classified_id
    data = {"status": "rejected"}

    access_token = await get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = host_url + f"/admin/classifieds/{classified_id}/"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url, json=data) as response:
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

            await callback_query.message.edit_caption()
            if currency_type == "usd":
                price = f"${price}"
            else:
                price = f"{price} so'm"

            result_dynamic_fields = ""
            if dynamic_fields:
                for dynamic_field in dynamic_fields:
                    result_dynamic_fields += f"{dynamic_field['key']}: {dynamic_field['value']}\n"

            text = f"{title}\n{category}\n{status}\n{price}\n{description}\n{location}\n{created_at}"

            if result_dynamic_fields:
                text += result_dynamic_fields

            markup = delete_classified(classified_id)

            await callback_query.message.edit_text(
                caption=text,
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN
            )


@router.callback_query(CheckStatus.filter(F.status == "delete"))
async def reject_classified(callback_query: types.CallbackQuery, callback_data: CheckStatus) -> None:
    classified_id = callback_data.classified_id
    data = {"status": "deleted"}

    access_token = await get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    url = host_url + f"/admin/classifieds/{classified_id}/"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch(url, json=data) as response:
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

            await callback_query.message.edit_caption()
            if currency_type == "usd":
                price = f"${price}"
            else:
                price = f"{price} so'm"

            result_dynamic_fields = ""
            if dynamic_fields:
                for dynamic_field in dynamic_fields:
                    result_dynamic_fields += f"{dynamic_field['key']}: {dynamic_field['value']}\n"

            text = f"{title}\n{category}\nStatus:{hbold(hcode(status))}\n{price}\n{description}\n{location}\n{created_at}"

            if result_dynamic_fields:
                text += result_dynamic_fields

            await callback_query.message.edit_text(
                caption=text,
                reply_markup=None,
                parse_mode=ParseMode.MARKDOWN
            )
