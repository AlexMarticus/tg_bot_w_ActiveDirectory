from aiogram import types

from keyboards.inline.back_to_start_menu import back_to_start
from loader import dp
from utils.db_func import task_info, take_tasks_id_to_check, who_is_executor


@dp.message_handler(commands="my_task_check")
async def my_task_check_func(message: types.Message):
    tasks_id = await take_tasks_id_to_check(message.from_user.id)
    if tasks_id:
        for i in tasks_id:
            task = await task_info(i)
            executor = await who_is_executor(i)
            answer = f"""-----{task[5]}-----
Описание: {task[6]}

Исполнитель: {' '.join(executor)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дата сдачи: {task[4].strftime("%d-%m-%Y")}
Дедлайн: {task[3].strftime("%d-%m-%Y")}
Ответ: {task[8]}

"""
            await message.answer(answer)
            if task[9] is not None:
                await message.answer_document(open(task[9], 'rb'))
            await message.answer('Для одобрения выполненной задачи: /completed\nДля отправки на переработку: /rework',
                                 reply_markup=back_to_start)
    else:
        await message.answer('Все задачи проверены!', reply_markup=back_to_start)


@dp.callback_query_handler(text="my_task_check")
async def my_task_check_func(call: types.CallbackQuery):
    tasks_id = await take_tasks_id_to_check(call.from_user.id)
    if tasks_id:
        for i in tasks_id:
            task = await task_info(i)
            executor = await who_is_executor(i)
            answer = f"""-----{task[5]}-----
Описание: {task[6]}

Исполнитель: {' '.join(executor)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дата сдачи: {task[4].strftime("%d-%m-%Y")}
Дедлайн: {task[3].strftime("%d-%m-%Y")}
Ответ: {task[8]}

"""
            await call.message.answer(answer)
            if task[9] is not None:
                await call.message.answer_document(open(task[9], 'rb'))
        await call.message.answer('Для одобрения выполненной задачи: /completed\nДля отправки на переработку: '
                                  '/rework', reply_markup=back_to_start)
    else:
        await call.message.edit_text('Все задачи проверены!', reply_markup=back_to_start)
