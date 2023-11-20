import sys
import asyncio
import logging

from decouple import config

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


from handlers.commands import router as command_router
# from handlers.callback_query import router as callback_query_router

TOKEN = config("BOT_TOKEN")

dp = Dispatcher()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.include_router(command_router)
    # dp.include_router(callback_query_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
