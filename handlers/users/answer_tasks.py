import datetime
import io
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.start_inl_bt import start_menu
from loader import dp
from states.answer_state import Answer
from utils.db_func import take_task_id_from_title, set_verif_task, take_answer_tasks_id_for_user


@dp.message_handler(commands="task")
async def task_answer(message: types.Message, state: FSMContext):
    tasks_id = await take_answer_tasks_id_for_user(message.from_user.id)
    if tasks_id:
        async with state.proxy() as data:
            data['ref10'] = tasks_id
        await message.answer('Введите навзание задачи, которую хотите выполнить или "отмена" для возврата в главное '
                             'меню')

        await Answer.title.set()
    else:
        await message.answer('Все задачи выполнены!', reply_markup=start_menu)


@dp.callback_query_handler(text="task")
async def task_answer_cb(call: types.CallbackQuery, state: FSMContext):
    tasks_id = await take_answer_tasks_id_for_user(call.from_user.id)
    await call.answer(cache_time=60)
    if tasks_id:
        async with state.proxy() as data:
            data['ref10'] = tasks_id
        await call.message.edit_text('Введите навзание задачи, которую хотите выполнить или "отмена" для возврата в '
                                     'главное меню')

        await Answer.title.set()
    else:
        await call.message.edit_text('Все задачи выполнены!', reply_markup=start_menu)


@dp.message_handler(state=Answer.title)
async def task_answer_title(message: types.Message, state: FSMContext):
    if message.text.lower() != 'отмена':
        async with state.proxy() as data:
            tasks_id = data['ref10']
        if await take_task_id_from_title(message.text) in tasks_id:
            await message.answer('Введите ответ на задачу, которую хотите выполнить '
                                 'или "отмена" для возврата в главное меню')
            async with state.proxy() as data:
                data['ref10'] = message.text
            await Answer.text.set()
        else:
            await state.reset_state(with_data=False)
            await message.answer('Такого названия у ваших задач нет.', reply_markup=start_menu)
    else:
        await message.answer('Возврат в главное меню', reply_markup=start_menu)
        await state.reset_state(with_data=False)


@dp.message_handler(state=Answer.text)
async def task_answer_text(message: types.Message, state: FSMContext):
    if message.text.lower() != 'отмена':
        async with state.proxy() as data:
            data['ref11'] = message.text
        await message.answer('Отправьте файл на задачу, которую хотите выполнить, "нет" для отправки ответа без файла '
                             'или "отмена" для возврата в главное меню')
        await Answer.file.set()
    else:
        await message.answer('Возврат в главное меню', reply_markup=start_menu)
        await state.reset_state(with_data=False)


@dp.message_handler(content_types=['photo', 'document'], state=Answer.file)
async def photo_or_doc_handler(message: types.Message, state: FSMContext):
    try:
        if message.text.lower() == 'отмена':
            await message.answer('Возврат в главное меню', reply_markup=start_menu)
            await state.reset_state(with_data=False)
        elif message.text.lower() == 'нет':
            async with state.proxy() as data:
                title = data['ref10']
                text = data['ref11']
            await set_verif_task(title, text)
            await state.reset_state(with_data=False)
            await message.answer('Успешно.', reply_markup=start_menu)
    except AttributeError:
        file_in_io = io.BytesIO()
        if message.content_type == 'photo':
            await message.photo[-1].download(destination_file=file_in_io)
        elif message.content_type == 'document':
            await message.document.download(destination_file=file_in_io)
        async with state.proxy() as data:
            title = data['ref10']
            text = data['ref11']
        date = '_'.join('_'.join('_'.join(str(datetime.datetime.now()).split()).split(':')).split('.'))
        file_name = f"{'_'.join(title.split())}__{date}"
        path = os.path.join('files_for_completed_tasks', file_name)
        with open(path, 'wb') as out:
            out.write(file_in_io.read())
        await set_verif_task(title, text, path)
        await state.reset_state(with_data=False)
        await message.answer('Успешно.', reply_markup=start_menu)
