from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import CheckStatus


def approve_or_reject(classified_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Tasdiqlash",
        callback_data=CheckStatus(
            status="approve",
            classified_id=classified_id
        ).pack()
    )
    builder.button(
        text="Rad etish",
        callback_data=CheckStatus(
            status="reject",
            classified_id=classified_id
        ).pack()
    )

    builder.adjust(2)
    return builder.as_markup()


def delete_classified(classified_id):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="O'chirish",
        callback_data=f'delete_{classified_id}'
    )

    builder.adjust(1)
    return builder.as_markup()
