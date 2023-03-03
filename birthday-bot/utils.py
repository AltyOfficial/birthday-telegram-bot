import calendar
import datetime
import const

from telegram import InlineKeyboardButton
import birthdays


def get_month_calendar(month):
    """Генерирует строку с календарем месяца текущего года."""

    weekdays = {
        'Mo': 'Пн',
        'Tu': 'Вт',
        'We': 'Ср',
        'Th': 'Чт',
        'Fr': 'Пт',
        'Sa': 'Сб',
        'Su': 'Вс',
    }

    year = datetime.date.today().year
    month_value = const.MONTH_NUM[month]['rus']
    text = f'{month_value} {year} 🗓\n<code>'

    data = calendar.month(year, month)
    data = data[data.find('Mo'):]
    today = str(datetime.date.today().day)

    if month == datetime.date.today().month:
        data = data.replace(f'{today}', f'</code><u>{today}</u><code>', 1)

    for en, ru in weekdays.items():
        data = data.replace(en, ru)

    text += data
    final = f'{text}</code>'

    return final


def make_calendar_keyboard(month_data):
    """Генерирует инлайн клавиатуру."""

    keyboard = [
        [
            InlineKeyboardButton(
                '⬅️ ' + month_data['left']['ru'],
                callback_data=month_data['left']['en']
            ),
            InlineKeyboardButton(
                month_data['right']['ru'] + ' ➡️',
                callback_data=month_data['right']['en']
            ),
        ],
    ]
    return keyboard


async def make_response(chat_id, month_num):
    """Генерирует сообщение с ответом."""

    items = await birthdays.get_birthday_list(chat_id, month_num)

    current_day = datetime.date.today().day
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    day_list = (12, 112, 13, 113, 14, 114,)


    if len(items) == 0:
        response = 'Список дней рождения в этом месяце пуст.'
    else:
        response = 'Список дней рождения:\n'
        for index, birthday in enumerate(items):
            day = str(int(birthday.date[:2]))
            month = const.MONTH_NUM[int(birthday.date[3:5])]['in_text']
            year = birthday.date[6:]

            age = current_year - int(year)

            if age % 10 == 1 and age != 11:
                end_string = 'год'
            elif age % 10 in (2, 3, 4) and age not in day_list:
                end_string = 'года'
            else:
                end_string = 'лет'

            info = f'{age} {end_string}'

            if month_num == current_month:
                if current_day == int(day):
                    info = f'сегодня исполняется {age} {end_string}!'
                elif current_day < int(day):
                    info = f'в этом месяце исполнится {age} {end_string}!'


            response += (
                f'<code>{index + 1}.</code> <b>{day} {month}</b> ' 
                f'- <b>{birthday.name}</b> - {info}\n'
            )
    
    text = get_month_calendar(month_num) + '\n' + response

    return text
