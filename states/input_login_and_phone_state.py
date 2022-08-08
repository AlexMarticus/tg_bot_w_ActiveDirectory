from aiogram.dispatcher.filters.state import StatesGroup, State


class LoginPhone(StatesGroup):
    login = State()
    phone = State()
