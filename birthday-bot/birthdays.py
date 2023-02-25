from dataclasses import dataclass
from datetime import datetime
import aiosqlite
import conf


@dataclass
class Birthday:
    id: int
    user_id: int
    name: str
    date: datetime


# async def get_bday_list():
#     result = []
#     async with aiosqlite.connect(conf.DATABASE_FILE) as db:
#         async with db.execute("SELECT * FROM birthdays;") as cursor:
#             async for row in cursor:
#                 result.append(Birthday(
#                     id=row['id'],
#                     user_id=
#                 ))
