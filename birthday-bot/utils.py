import calendar
import datetime
import const


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
    today = str(datetime.date.today().day)

    if month == datetime.date.today().month:
        data = data.replace(f'{today}', f'</code><u>{today}</u><code>', 1)

    for en, ru in weekdays.items():
        data = data.replace(en, ru)

    text += data[data.find('Пн'):]
    final = f'{text}</code>'

    return final