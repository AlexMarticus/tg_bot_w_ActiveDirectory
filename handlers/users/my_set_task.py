import asyncio
import datetime

import aioschedule
from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.users.start import bot_start
from keyboards.inline.start_inl_bt import start_menu
from loader import dp, bot
from states.set_task_state import SetTask
from utils.db_func import take_user_id_from_name_surname, add_task, add_executor__task, take_task_id_from_title, \
    is_title_uniq, take_user_id_from_tg_id, check_is_completed_task, take_tg_id_from_user_id


@dp.message_handler(commands="my_set_task")
async def my_set_task_func(message: types.Message):
    await message.answer('Введите имя и фамилию исполнителя через пробел или "отмена" для возврата в главное меню')
    await SetTask.NameSurname.set()


@dp.callback_query_handler(text="my_set_task")
async def my_set_task_func_cb(call: types.CallbackQuery):
    await call.message.edit_text('Введите имя и фамилию исполнителя через пробел или "отмена" для возврата в главное '
                                 'меню')
    await SetTask.NameSurname.set()


@dp.message_handler(state=SetTask.NameSurname)
async def set_task_name_surname(message: types.Message, state: FSMContext):
    if message.text.lower() != 'отмена':
        try:
            name, surname = message.text.split()
            user_id = await take_user_id_from_name_surname(name, surname)
            if user_id:
                async with state.proxy() as data:
                    data['ref10'] = user_id
                await message.answer('Введите заголовок задачи или "отмена" для возврата в главное меню')
                await SetTask.next()
            else:
                await state.reset_state(with_data=False)
                await message.answer('Данные введены не верно. Уточните их и попробуйте ещё раз.')
                await bot_start(message)
        except ValueError:
            await state.reset_state(with_data=False)
            await message.answer('Данные введены не верно. Уточните их и попробуйте ещё раз.')
            await bot_start(message)
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=SetTask.title)
async def set_task_title(message: types.Message, state: FSMContext):
    if message.text.lower() != 'отмена':
        title = message.text
        if await is_title_uniq(title) == 0:
            async with state.proxy() as data:
                data['ref11'] = title
            await message.answer('Введите описание задачи или "отмена" для возврата в главное меню')
            await SetTask.next()
        else:
            await message.answer('Такое название уже есть. Придумайте уникальное название и попробуйте ещё раз')
            await state.reset_state(with_data=False)
            await bot_start(message)
    else:
        await state.reset_state(with_data=False)
        await message.answer('Возврат в главное меню', reply_markup=start_menu)


@dp.message_handler(state=SetTask.description)
async def set_task_description(message: types.Message, state: FSMContext):
    if message.text.lower() != 'отмена':
        description = message.text
        async with state.proxy() as data:
            data['ref12'] = description
        await message.answer('Введите дедлайн задачи в формате гггг-мм-дд или "отмена" для возврата в главное меню')
        await SetTask.next()
    else:
        await state.reset_state(with_data=False)
        await message.answer('Возврат в главное меню', reply_markup=start_menu)


async def scheduler(time, task_id, user_id, title):
    await aioschedule.run_pending()
    await asyncio.sleep(time)
    if not await check_is_completed_task(task_id):
        await bot.send_message(chat_id=user_id, text=f'Остался 1 день до дедлайна задачи {title}.')


@dp.message_handler(state=SetTask.deadline)
async def set_task_deadline(message: types.Message, state: FSMContext):
    if message.text.lower() != 'отмена':
        deadline = message.text
        async with state.proxy() as data:
            user_id = data['ref10']
            title = data['ref11']
            description = data['ref12']
        await state.reset_state(with_data=False)
        if datetime.date(*list(map(lambda x: int(x), deadline.split('-')))) >= datetime.date.today():
            creator_id = await take_user_id_from_tg_id(message.from_user.id)
            await add_task(creator_id=creator_id,
                           title=title, description=description, date_now=datetime.date.today(), deadline=deadline)
            task_id = await take_task_id_from_title(title)
            await add_executor__task(user_id, task_id)
            tg_id = await take_tg_id_from_user_id(user_id)
            await bot.send_message(chat_id=tg_id, text='Вам прислали новое задание. '
                                                       'Просмотреть его: /for_me_new_tasks')
            if datetime.date(*list(map(lambda x: int(x), deadline.split('-')))) - datetime.timedelta(1) > \
                    datetime.date.today():
                time = datetime.date(*list(map(lambda x: int(x), deadline.split('-')))) - datetime.timedelta(1) \
                       - datetime.date.today()
                asyncio.create_task(scheduler(time.total_seconds(), task_id, user_id, title))
            await message.answer('Задача направлена исполнителю', reply_markup=start_menu)
        else:
            await message.answer('Мы пока не научились управлять временем.', reply_markup=start_menu)
    else:
        await state.reset_state(with_data=False)
        await message.answer('Возврат в главное меню', reply_markup=start_menu)
