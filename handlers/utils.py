import aiohttp
from datetime import timedelta, datetime

from decouple import config

from loader import dp

login = config("LOGIN")
password = config("PASSWORD")
host_url = config("HOST_URL")


async def get_access_token():
    data = await dp.storage.get_data()

    if not data:
        data = await retrieve_tokens()
    elif data["expiry"] < datetime.now():
        data = await refresh_tokens(data['refresh_token'])

    return data["access_token"]


async def get_refresh_token():
    data = await dp.storage.get_data()
    if not data:
        await retrieve_tokens()
    return data["refresh_token"]


async def retrieve_tokens():
    url = f"{host_url}/admin/login/"
    payload = {"userInput": login, "password": password}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()

            await dp.storage.set_data(data)

    return data


async def refresh_tokens(refresh_token):
    url = f"{host_url}/login/refresh/"
    payload = {"refresh": refresh_token}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()

            expires_in = data.get("expires_in", 7200)
            data["expiry"] = datetime.now() + timedelta(seconds=expires_in)

            await dp.storage.update_data(data)

    return data
