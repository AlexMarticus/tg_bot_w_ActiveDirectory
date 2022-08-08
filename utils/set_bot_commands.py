from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand('for_me_new_tasks', 'Новые задачи для Вас'),
            types.BotCommand('for_me_tasks', 'Задачи для Вас'),
            types.BotCommand('for_me_completed_tasks', 'Выполненные Вами задачи'),
            types.BotCommand('my_set_task', 'Поставить кому-либо задачу'),
            types.BotCommand('my_task_check', 'Задачи, ожидающие Вашей проверки'),
            types.BotCommand('my_assigned_tasks', 'Задачи, заданные мною'),
        ]
    )
