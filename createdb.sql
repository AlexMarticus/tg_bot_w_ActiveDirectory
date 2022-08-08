DROP TABLE IF EXISTS executor__task;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;


CREATE TABLE users
(
    user_id serial,
    name varchar(20) NOT NULL,
    surname varchar(20) NOT NULL,
    phone varchar(15) NOT NULL,
    tg_id int NOT NULL,
    login varchar(50) NOT NULL,

    CONSTRAINT PK_users_user_id PRIMARY KEY(user_id)
);

CREATE TABLE tasks
(
    task_id serial,
    creator int NOT NULL,
    creating_date date NOT NULL,
    deadline_date date NOT NULL,
    completed_date date,
    title text NOT NULL UNIQUE,
    description text DEFAULT 'Отсутствует',
    status varchar(12) NOT NULL DEFAULT 'given',
    text_answer text DEFAULT 'Отсутствует',
    path_to_file_answer text,
    
    CONSTRAINT FK_tasks_creator FOREIGN KEY(creator) REFERENCES users(user_id),
    CONSTRAINT CHK_tasks_status CHECK (status = 'given' OR status = 'verification' OR status = 'execution' OR status = 'rework' OR status = 'completed'),
    CONSTRAINT PK_tasks_task_id PRIMARY KEY(task_id)
);

CREATE TABLE executor__task
(
    user_id int REFERENCES users(user_id),
    task_id int REFERENCES tasks(task_id),
    
    CONSTRAINT PK_executor__task PRIMARY KEY(user_id, task_id)
);

ALTER DATABASE tg_w_AD OWNER TO bot;

INSERT INTO users (name, surname, phone, tg_id, login) VALUES ('Test_name', 'Test_surname', '+12345678910', 123456789, 'test_login');
INSERT INTO users (name, surname, phone, tg_id, login) VALUES ('Антон', 'Озеров', '+79196804453', 481317616, 'alex_mart3');
INSERT INTO users (name, surname, phone, tg_id, login) VALUES ('Алексей', 'Март', '+79115556677', 940652676, 'v.pupkin');
INSERT INTO users (name, surname, phone, tg_id, login) VALUES ('Никита', 'Курышев', '+78005553535', 1049866669, 'nikitos');
INSERT INTO tasks (creator, creating_date, deadline_date, completed_date, title, status) VALUES (1, '2022-08-01', '2022-08-01', '2022-08-01', 'Мышь', 'completed');
INSERT INTO tasks (creator, creating_date, deadline_date, title) VALUES (1, '2022-07-01', '2022-10-13', 'Сорока');
INSERT INTO tasks (creator, creating_date, deadline_date, title) VALUES (1, '2022-07-01', '2022-10-13', 'Медведь');
INSERT INTO executor__task VALUES (2, 1);
INSERT INTO executor__task VALUES (2, 2);
INSERT INTO executor__task VALUES (2, 3);
