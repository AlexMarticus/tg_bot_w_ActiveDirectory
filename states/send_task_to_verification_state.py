from aiogram.dispatcher.filters.state import StatesGroup, State


class Verification(StatesGroup):
    text_answer = State()
    file_answer = State()
