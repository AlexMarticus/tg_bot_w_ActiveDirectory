from aiogram.dispatcher.filters.state import StatesGroup, State


class SetTask(StatesGroup):
    NameSurname = State()
    title = State()
    description = State()
    deadline = State()
