from aiogram import types

from keyboards.inline.back_to_start_menu import back_to_start
from loader import dp
from utils.db_func import task_info, who_is_creator, take_user_s_tasks


@dp.message_handler(commands="my_assigned_tasks")
async def my_assigned_tasks_func(message: types.Message):
    tasks_id = await take_user_s_tasks(message.from_user.id)
    if tasks_id:
        answer = str()
        for i in tasks_id:
            task = await task_info(i)
            if task[7] == 'given':
                stat = 'Ожидает принятия исполнителем'
            elif task[7] == 'verification':
                stat = 'Отправлена на проверку'
            elif task[7] == 'execution':
                stat = 'Выполняется исполнителем'
            elif task[7] == 'rework':
                stat = 'Отправлена на доработку'
            else:
                stat = 'Выполнено успешно'
            creator_name = await who_is_creator(task[1])
            answer += f"""-----{task[5]}-----
Описание: {task[6]}

Заказчик: {' '.join(creator_name)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дедлайн: {task[3].strftime("%d-%m-%Y")}
Статус: {stat}


"""
        await message.answer(answer, reply_markup=back_to_start)
    else:
        await message.answer('Все задачи выполнены!', reply_markup=back_to_start)


@dp.callback_query_handler(text="my_assigned_tasks")
async def my_assigned_tasks_func(call: types.CallbackQuery):
    tasks_id = await take_user_s_tasks(call.from_user.id)
    if tasks_id:
        answer = str()
        for i in tasks_id:
            task = await task_info(i)
            if task[7] == 'given':
                stat = 'Ожидает принятия исполнителем'
            elif task[7] == 'verification':
                stat = 'Отправлена на проверку'
            elif task[7] == 'execution':
                stat = 'Выполняется исполнителем'
            elif task[7] == 'rework':
                stat = 'Отправлена на доработку'
            else:
                stat = 'Выполнено успешно'
            creator_name = await who_is_creator(task[1])
            answer += f"""-----{task[5]}-----
Описание: {task[6]}

Заказчик: {' '.join(creator_name)}
Дата создания: {task[2].strftime("%d-%m-%Y")}
Дедлайн: {task[3].strftime("%d-%m-%Y")}
Статус: {stat}


"""
        await call.message.edit_text(answer, reply_markup=back_to_start)
    else:
        await call.message.edit_text('Все задачи выполнены!', reply_markup=back_to_start)
