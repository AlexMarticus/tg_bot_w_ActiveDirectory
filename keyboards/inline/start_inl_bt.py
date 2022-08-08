from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Новые задачи", callback_data="for_me_new_tasks"),
        InlineKeyboardButton(text="Задачи для меня", callback_data="for_me_tasks"),
    ],
    [
        InlineKeyboardButton(text="Отправить на проверку", callback_data="task"),
        InlineKeyboardButton(text="Мною выполненные задачи", callback_data="for_me_completed_tasks"),
    ],
    [
        InlineKeyboardButton(text="Задачи для проверки", callback_data="my_task_check"),
        InlineKeyboardButton(text="Задачи от меня", callback_data="my_assigned_tasks"),
    ],
    [
        InlineKeyboardButton(text="Задать задачу", callback_data="my_set_task"),
    ],
])
