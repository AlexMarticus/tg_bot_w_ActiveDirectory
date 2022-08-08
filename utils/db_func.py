import datetime

import psycopg
from data.config import PG_USER, DB_NAME, PG_PASS


async def who_is_creator(user_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT (name, surname) FROM users WHERE user_id = %s", (user_id,))
            full_name = (await acur.fetchone())[0]
            return full_name


async def check_is_new_user(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT count(user_id) FROM users WHERE tg_id = %s", (tg_id,))
            count = await acur.fetchone()
            if count[0] != 1:
                return 'new'
            return False


async def add_new_user(tg_id, login, phone, name, surname):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.transaction() as acur:
            await acur.execute('''INSERT INTO users (tg_id, login, phone name, surname) VALUES (%s, %s, %s, %s, %s)''',
                               (tg_id, login, phone, name, surname,))
            await aconn.commit()


async def task_info(task_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('''SELECT * FROM tasks WHERE task_id = %s''', (task_id,))
            info = await acur.fetchone()
    return info


async def take_tasks_id_for_user(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            user_id = (await acur.fetchone())[0]
            await acur.execute("SELECT task_id FROM executor__task WHERE user_id = %s", (user_id,))
            tasks_id = list(map(lambda x: x[0],
                                await acur.fetchall()))
            not_new_and_not_completed_tasks_id = []
            for task_id in tasks_id:
                if not await check_is_new_task(task_id) and not await check_is_completed_task(task_id):
                    not_new_and_not_completed_tasks_id.append(task_id)
    if not_new_and_not_completed_tasks_id:
        return not_new_and_not_completed_tasks_id
    return False


async def take_answer_tasks_id_for_user(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            user_id = (await acur.fetchone())[0]
            await acur.execute("SELECT task_id FROM executor__task WHERE user_id = %s", (user_id,))
            tasks_id = list(map(lambda x: x[0],
                                await acur.fetchall()))
            not_new_and_not_completed_tasks_id = []
            for task_id in tasks_id:
                if not await check_is_new_task(task_id) and not await check_is_completed_task(task_id)\
                        and not await check_is_ver_task(task_id):
                    not_new_and_not_completed_tasks_id.append(task_id)
    if not_new_and_not_completed_tasks_id:
        return not_new_and_not_completed_tasks_id
    return False


async def take_completed_tasks_id_for_user(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            user_id = (await acur.fetchone())[0]
            await acur.execute("SELECT task_id FROM executor__task WHERE user_id = %s", (user_id,))
            tasks_id = list(map(lambda x: x[0],
                                await acur.fetchall()))
            completed_tasks_id = []
            for task_id in tasks_id:
                if await check_is_completed_task(task_id):
                    completed_tasks_id.append(task_id)
    if completed_tasks_id:
        return completed_tasks_id
    return False


async def take_user_id_from_tg_id(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            user_id = (await acur.fetchone())[0]
            return user_id


async def take_tg_id_from_user_id(user_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT tg_id FROM users WHERE user_id = %s", (user_id,))
            tg_id = (await acur.fetchone())[0]
            return tg_id


async def is_title_uniq(title):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT count(task_id) FROM tasks WHERE title = %s", (title,))
            task_id = (await acur.fetchone())[0]
            return task_id


async def take_task_id_from_title(title):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT task_id FROM tasks WHERE title = %s", (title,))
            try:
                task_id = (await acur.fetchone())[0]
                return task_id
            except TypeError:
                return False


async def add_task(creator_id, date_now, title, description, deadline):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("INSERT INTO tasks (creator, creating_date, deadline_date, title, description) "
                               "VALUES (%s, %s, %s, %s, %s)",
                               (creator_id, date_now, deadline, title, description,))
            await aconn.commit()


async def add_executor__task(user_id, task_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("INSERT INTO executor__task (user_id, task_id) VALUES (%s, %s)", (user_id, task_id,))
            await aconn.commit()


async def take_user_id_from_name_surname(name, surname):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            try:
                await acur.execute("SELECT user_id FROM users WHERE name = %s AND surname = %s", (name, surname,))
                user_id = (await acur.fetchone())[0]
                return user_id
            except TypeError:
                return False


async def take_new_tasks_id_for_user_and_change_status(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            user_id = (await acur.fetchone())[0]
            await acur.execute("SELECT task_id FROM executor__task WHERE user_id = %s", (user_id,))
            tasks_id = list(map(lambda x: x[0],
                                await acur.fetchall()))
            new_task_id = []
            for task_id in tasks_id:
                if await check_is_new_task(task_id):
                    new_task_id.append(task_id)
                    await acur.execute("UPDATE tasks SET status = 'execution' WHERE task_id = %s", (task_id,))
            await aconn.commit()
    if new_task_id:
        return new_task_id
    return False


async def check_is_new_task(task_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('''SELECT status FROM tasks WHERE task_id = %s''', (task_id,))
            status = (await acur.fetchone())[0]
    if status == 'given':
        return True
    return False


async def check_is_ver_task(task_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('''SELECT status FROM tasks WHERE task_id = %s''', (task_id,))
            status = (await acur.fetchone())[0]
    if status == 'verification':
        return True
    return False


async def check_is_completed_task(task_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute('''SELECT status FROM tasks WHERE task_id = %s''', (task_id,))
            status = (await acur.fetchone())[0]
    if status == 'completed':
        return True
    return False


async def who_is_executor(task_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM executor__task WHERE task_id = %s", (task_id,))
            user_id = (await acur.fetchone())[0]
            await acur.execute("SELECT (name, surname) FROM users WHERE user_id = %s", (user_id,))
            full_name = (await acur.fetchone())[0]
            return full_name


async def set_completed_task(title):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("UPDATE tasks SET status = 'completed' WHERE title = %s", (title,))
            await aconn.commit()


async def set_rework_task(title):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("UPDATE tasks SET status = 'rework' WHERE title = %s", (title,))
            await aconn.commit()


async def set_verif_task(title, text, path=None):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("""UPDATE tasks SET status = 'verification', 
text_answer = %s, path_to_file_answer = %s, completed_date = %s WHERE title = %s""",
                               (text, path, datetime.datetime.now(), title,))
            await aconn.commit()


async def take_verif_tasks_to_complet(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            creator = (await acur.fetchone())[0]
            await acur.execute("SELECT title FROM tasks WHERE creator = %s AND status = 'verification'", (creator,))
            tasks_id = list(map(lambda x: x[0],
                                await acur.fetchall()))
            if tasks_id:
                return tasks_id
            else:
                return False


async def take_tasks_id_to_check(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            user_id = (await acur.fetchone())[0]
            await acur.execute("SELECT task_id FROM tasks WHERE creator = %s AND status = 'verification'", (user_id,))
            tasks_id = list(map(lambda x: x[0],
                                await acur.fetchall()))
            if tasks_id:
                return tasks_id
            else:
                return False


async def take_user_s_tasks(tg_id):
    async with await psycopg.AsyncConnection.connect(f"dbname={DB_NAME} user={PG_USER} password={PG_PASS}") as aconn:
        async with aconn.cursor() as acur:
            await acur.execute("SELECT user_id FROM users WHERE tg_id = %s", (tg_id,))
            user_id = (await acur.fetchone())[0]
            await acur.execute("SELECT task_id FROM tasks WHERE creator = %s", (user_id,))
            tasks_id = list(map(lambda x: x[0],
                                await acur.fetchall()))
            if tasks_id:
                return tasks_id
            else:
                return False
