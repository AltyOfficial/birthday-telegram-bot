CREATE TABLE IF NOT EXISTS birthdays (
    id INTEGER PRIMARY KEY,
    user_id BIGINT,
    name VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    ordering INTEGER NOT NULL
);


# Для создания базы данных - cat db.sql | sqlite3 database_name.sqlite3
# Для просмотра таблиц - .tables
# Для просмотра полей таблицы - SELECT name FROM PRAGMA_TABLE_INFO('your_table');