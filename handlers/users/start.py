from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.start_inl_bt import start_menu
from loader import dp
from states.input_login_and_phone_state import LoginPhone
from utils.db_func import check_is_new_user, add_new_user
from utils.work_with_ActiveDirectory import find_ad_users


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    is_new = await check_is_new_user(message.from_user.id)
    if is_new:
        await message.answer("""Доброго времени суток! Введите Ваш логин.""")
        await LoginPhone.login.set()
    else:
        await message.answer("""Выберите нужный Вам пункт""", reply_markup=start_menu)


@dp.message_handler(state=LoginPhone.login)
async def get_login(message: types.Message, state: FSMContext):
    login = message.text
    login = [login]
    async with state.proxy() as data:
        data['ref10'] = login
    await message.answer('Введите Ваш номер телефона в формате +79995554400.')
    await LoginPhone.phone.set()


@dp.message_handler(state=LoginPhone.phone)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        login = data['ref10']
    await state.reset_state(with_data=False)
    if find_ad_users(username=login, phone=message.text):
        await add_new_user(tg_id=message.from_user.id, login=login, phone=message.text,)
        await message.answer("Вход выполнен успешно.")
    else:
        await message.answer('Введенные данные не найдены в нашей системе. '
                             'Уточните их у <change> и попробуйте ещё раз.')


@dp.callback_query_handler(text="back_to_start")
async def back_to_start(call: types.CallbackQuery):
    is_new = await check_is_new_user(call.from_user.id)
    if is_new:
        await call.message.answer("""Доброго времени суток! Введите Ваш логин.""")
        await LoginPhone.login.set()
    else:
        await call.message.edit_text("""Выберите нужный Вам пункт""", reply_markup=start_menu)
