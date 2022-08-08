from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import bot_start
from loader import dp
from states.completed_task_state import ToComplet
from utils.db_func import take_verif_tasks_to_complet, set_completed_task


@dp.message_handler(commands="completed")
async def completed_task_func(message: types.Message, state: FSMContext):
    tasks_titles = await take_verif_tasks_to_complet(message.from_user.id)
    if tasks_titles:
        async with state.proxy() as data:
            data['ref10'] = tasks_titles
        await message.answer('Введите навзание задачи для подтверждения принятия или "отмена" для возврата в главное '
                             'меню')
        await ToComplet.Name.set()
    else:
        await message.answer('У Вас нет задач на проверке.')


@dp.message_handler(state=ToComplet.Name)
async def set_task_deadline(message: types.Message, state: FSMContext):
    if message.text.lower() != 'отмена':
        async with state.proxy() as data:
            tasks_titles = data['ref10']
        await state.reset_state(with_data=False)
        if message.text in tasks_titles:
            await set_completed_task(message.text)
            await message.answer('Успешно')
        else:
            await message.answer('Такого названия у ваших задач нет.')
    else:
        await state.reset_state(with_data=False)
    await bot_start(message)
