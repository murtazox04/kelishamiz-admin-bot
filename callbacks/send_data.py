from aiogram.filters.callback_data import CallbackData


class CheckStatus(CallbackData, prefix="classified"):
    status: str
    classified_id: int
