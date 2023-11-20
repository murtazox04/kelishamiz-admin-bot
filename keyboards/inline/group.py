from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def approve_or_reject():
    builder = InlineKeyboardBuilder()

    builder.button(text="Tasdiqlash", callback_data='approve')
    builder.button(text="Rad etish", callback_data='reject')

    builder.adjust(2)
    return builder.as_markup()
