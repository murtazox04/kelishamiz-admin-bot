import aiohttp

from decouple import config
from datetime import datetime

from database import Tokens
from loader import TOKEN

tokens = Tokens()

login = config("LOGIN")
password = config("PASSWORD")
host_url = config("HOST_URL")


async def get_access_token():
    token_data = await tokens.read(bot_token=TOKEN)

    if not token_data:
        token_data = await retrieve_tokens()
    elif token_data["expires_at"] < datetime.now():
        token_data = await refresh_tokens(token_data['refresh_token'])
    return token_data["access_token"]


async def get_refresh_token():
    token_data = await tokens.read(bot_token=TOKEN)

    if not token_data:
        await retrieve_tokens()

    return token_data["refresh_token"]


async def retrieve_tokens():
    url = f"{host_url}/admin/login/"
    payload = {"userInput": login, "password": password}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()

            data = await tokens.insert(
                access_token=data['access'],
                refresh_token=data['refresh']
            )

    return data


async def refresh_tokens(refresh_token):
    url = f"{host_url}/login/refresh/"
    payload = {"refresh": refresh_token}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()

            data = await tokens.update(
                bot_token=TOKEN,
                access_token=data['access'],
            )

    return data
