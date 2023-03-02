from dataclasses import dataclass
from datetime import datetime
import aiosqlite
import conf


@dataclass
class Birthday:
    user_id: int
    name: str
    date: datetime


async def get_birthday_list(user_id, month_num=None):
    """Функция для взятия данных из базы."""

    result = []

    db = await aiosqlite.connect(conf.DATABASE_FILE)
    db.row_factory = aiosqlite.Row

    if len(str(month_num)) == 1:
        month_num = '0' + str(month_num)

    command = 'SELECT * FROM birthdays WHERE user_id = ? and date LIKE ?;'
    cursor = await db.execute(command, (user_id, f'%.{month_num}.%',))

    async for row in cursor:
        result.append(Birthday(
            user_id=row['user_id'],
            name=row['name'],
            date=row['date'],
        ))

    await db.close()

    return result


async def get_bday_list(user_id):
    result = []
    db = await aiosqlite.connect(conf.DATABASE_FILE)
    db.row_factory = aiosqlite.Row
    command = 'SELECT * FROM birthdays WHERE user_id = ? and date LIKE ?;'
    cursor = await db.execute(command, (user_id, '%.02.%'))
    # command = 'SELECT * FROM birthdays WHERE user_id = ?;'
    # cursor = await db.execute(command, (user_id,))
    async for row in cursor:
        result.append(Birthday(
            user_id=row['user_id'],
            name=row['name'],
            date=row['date'],
        ))
    await db.close()
    return result
    # result = []
    # async with aiosqlite.connect(conf.DATABASE_FILE) as db:
    #     db.row_factory = aiosqlite.Row
    #     async with db.execute("SELECT * FROM birthdays;") as cursor:
    #         async for row in cursor:
    #             result.append(Birthday(
    #                 user_id=row['user_id'],
    #                 name=row['name'],
    #                 date=row['date']
    #             ))
    # return result


async def add_bday(chat_id, name, date):
    db = await aiosqlite.connect(conf.DATABASE_FILE)
    command = (
        'INSERT INTO birthdays (user_id, name, date, ordering)'
        'VALUES (?, ?, ?, 4);'
    )
    await db.execute(command, (chat_id, name, date))
    await db.commit()
    await db.close()
    return


async def delete_birthday(chat_id, month, index):
    db = await aiosqlite.connect(conf.DATABASE_FILE)
    command = (
        'DELETE FROM birthdays WHERE user_id = ? AND name = ? AND date = ?;'
    )
    await db.commit()
    await db.close()
    return

