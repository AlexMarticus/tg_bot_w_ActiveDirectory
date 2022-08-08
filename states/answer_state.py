from aiogram.dispatcher.filters.state import StatesGroup, State


class Answer(StatesGroup):
    title = State()
    text = State()
    file = State()
