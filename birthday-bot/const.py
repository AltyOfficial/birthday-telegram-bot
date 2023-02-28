import utils


MONTH = {
    'Январь': {
        # 'rus': 'Январь',
        'calendar': utils.get_month_calendar(1),
        'left': 'Декабрь',
        'right': 'Февраль',
    },
    'Февраль': {
        # 'rus': 'Февраль',
        'calendar': utils.get_month_calendar(2),
        'left': 'Январь',
        'right': 'Март',
    },
    'Март': {
        # 'rus': 'Март',
        'calendar': utils.get_month_calendar(3),
        'left': 'Февраль',
        'right': 'Апрель',
    },
    # 'April': 'Апрель',
    # 'May': 'Май',
    # 'June': 'Июнь',
    # 'Jule': 'Июль',
    # 'August': 'Август',
    # 'September': 'Сентябрь',
    # 'October': 'Октябрь',
    # 'November': 'Ноябрь',
    # 'December': 'Декабрь',
}