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

    cond = False
    if month == datetime.date.today().month:
        cond = True

    data = calendar.month(year, month)
    for en, ru in weekdays.items():
        data = data.replace(en, ru)

    text += data[data.find('Пн'):]
    today = str(datetime.date.today().day)

    if cond:
        text = text.replace(f'{today}', f'</code><u>{today}</u><code>', 1)

    final = f'{text}</code>'

    return final