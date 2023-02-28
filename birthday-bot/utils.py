import calendar
import datetime


def get_month_calendar(month):
    year = datetime.date.today().year
    month = calendar.month(year, month)
    today = str(datetime.date.today().day)
    month = month.replace(f'{today}', f'</code><u>{today}</u><code>')
    text = f'<code>{month}</code>'
    return text