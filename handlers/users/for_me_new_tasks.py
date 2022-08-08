from aiogram import types

from keyboards.inline.back_to_start_menu import back_to_start
from loader import dp
from utils.db_func import take_new_tasks_id_for_user_and_change_status, task_info, who_is_creator


@dp.message_handler(commands="for_me_new_tasks")
async def for_me_new_tasks_func(message: types.Message):
    tasks_id = await take_new_tasks_id_for_user_and_change_status(message.from_user.id)
    if tasks_id:
        answer = str()
        for i in tasks_id:
            task = await task_info(i)
            creator_name = await who_is_creator(task[1])
            answer += f"""-----{task[5]}-----
Описание: {task[6]}

Заказчик: {' '.join(creator_name)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дедлайн: {task[3].strftime("%d-%m-%Y")}


"""
        await message.answer(answer, reply_markup=back_to_start)
    else:
        await message.answer('Новых задач нет', reply_markup=back_to_start)


@dp.callback_query_handler(text="for_me_new_tasks")
async def for_me_new_tasks_func_cb(call: types.CallbackQuery):
    tasks_id = await take_new_tasks_id_for_user_and_change_status(call.from_user.id)
    if tasks_id:
        answer = str()
        for i in tasks_id:
            task = await task_info(i)
            creator_name = await who_is_creator(task[1])
            answer += f"""-----{task[5]}-----
Описание: {task[6]}

Заказчик: {' '.join(creator_name)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дедлайн: {task[3].strftime("%d-%m-%Y")}


"""
        await call.message.edit_text(answer, reply_markup=back_to_start)
    else:
        await call.message.edit_text('Новых задач нет', reply_markup=back_to_start)
