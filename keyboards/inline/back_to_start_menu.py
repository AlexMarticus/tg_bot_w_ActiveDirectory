from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад в меню", callback_data="back_to_start"),
    ],
])
