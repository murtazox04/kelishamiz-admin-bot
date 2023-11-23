from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext

from handlers.group import event_chats
from handlers.commands import router as command_router
from handlers.callback_query import router as callback_query_router
from loader import app, dp, bot, WEBHOOK_PATH, WEBHOOK_URL


@app.on_event("startup")
async def on_startup() -> None:
    dp.include_router(callback_query_router)
    dp.include_router(command_router)
    url = await bot.get_webhook_info()

    if url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict) -> None:
    telegram_update = types.Update(**update)
    await Dispatcher._feed_webhook_update(
        self=dp,
        bot=bot,
        update=telegram_update
    )


@app.post("/new-classified")
async def new_classified(classified: dict) -> None:
    if classified:
        classified_id = classified['id']
        title = classified['title']
        category = classified['category']
        currency_type = classified['detail']['currencyType']
        price = classified['detail']['price']
        status = classified['status']
        description = classified['detail']['description']
        dynamic_fields = classified['detail']['dynamicFields']
        location = classified['detail']['location']
        images = classified['detail']['images']
        created_at = classified['createdAt']

        await event_chats.send_chat_data(
            classified_id=classified_id,
            title=title,
            category=category,
            status=status,
            currency_type=currency_type,
            price=price,
            description=description,
            dynamic_fields=dynamic_fields,
            images=images,
            location=location,
            created_at=created_at
        )


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await dp.storage.close()
