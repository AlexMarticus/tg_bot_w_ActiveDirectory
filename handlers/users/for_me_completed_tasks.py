from aiogram import types

from keyboards.inline.back_to_start_menu import back_to_start
from loader import dp
from utils.db_func import task_info, who_is_creator, take_completed_tasks_id_for_user


@dp.message_handler(commands="for_me_completed_tasks")
async def for_me_completed_tasks_func(message: types.Message):
    tasks_id = await take_completed_tasks_id_for_user(message.from_user.id)
    if tasks_id:
        for i in tasks_id:
            task = await task_info(i)
            creator_name = await who_is_creator(task[1])
            answer = f"""-----{task[5]}-----
Описание: {task[6]}

Заказчик: {' '.join(creator_name)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дата выполнения: {task[4].strftime("%d-%m-%Y")}
Ответ: {task[8]}


"""
            await message.answer(answer)
            if task[9] is not None:
                await message.answer_document(open(task[9], 'rb'))
        await message.answer('Главное меню', reply_markup=back_to_start)
    else:
        await message.answer('Пока выполненных задач нет', reply_markup=back_to_start)


@dp.callback_query_handler(text="for_me_completed_tasks")
async def for_me_completed_tasks_func_cb(call: types.CallbackQuery):
    tasks_id = await take_completed_tasks_id_for_user(call.from_user.id)
    if tasks_id:
        for i in tasks_id:
            task = await task_info(i)
            creator_name = await who_is_creator(task[1])
            answer = f"""-----{task[5]}-----
Описание: {task[6]}

Заказчик: {' '.join(creator_name)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дата выполнения: {task[4].strftime("%d-%m-%Y")}
Ответ: {task[8]}


"""
            await call.message.edit_text(answer)
            if task[9] is not None:
                await call.message.answer_document(open(task[9], 'rb'))
            await call.message.answer('Главное меню', reply_markup=back_to_start)
    else:
        await call.message.edit_text('Пока выполненных задач нет', reply_markup=back_to_start)
