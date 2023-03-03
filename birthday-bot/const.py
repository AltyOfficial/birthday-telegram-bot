import collections


MONTH = {
    'January': {
        'rus': 'Январь',
        'num': 1,
        'left': {
            'en': 'December',
            'ru': 'Декабрь',
        },
        'right': {
            'en': 'February',
            'ru': 'Февраль',
        },
    },
    'February': {
        'rus': 'Февраль',
        'num': 2,
        'left': {
            'en': 'January',
            'ru': 'Январь',
        },
        'right': {
            'en': 'March',
            'ru': 'Март',
        },
    },
    'March': {
        'rus': 'Март',
        'num': 3,
        'left': {
            'en': 'February',
            'ru': 'Февраль',
        },
        'right': {
            'en': 'April',
            'ru': 'Апрель',
        },
    },
    'April': {
        'rus': 'Апрель',
        'num': 4,
        'left': {
            'en': 'March',
            'ru': 'Март',
        },
        'right': {
            'en': 'May',
            'ru': 'Май',
        },
    },
    'May': {
        'rus': 'Май',
        'num': 5,
        'left': {
            'en': 'April',
            'ru': 'Апрель',
        },
        'right': {
            'en': 'June',
            'ru': 'Июнь',
        },
    },
    'June': {
        'rus': 'Июнь',
        'num': 6,
        'left': {
            'en': 'May',
            'ru': 'Май',
        },
        'right': {
            'en': 'July',
            'ru': 'Июль',
        },
    },
    'July': {
        'rus': 'Июль',
        'num': 7,
        'left': {
            'en': 'June',
            'ru': 'Июнь',
        },
        'right': {
            'en': 'August',
            'ru': 'Август',
        },
    },
    'August': {
        'rus': 'Август',
        'num': 8,
        'left': {
            'en': 'July',
            'ru': 'Июль',
        },
        'right': {
            'en': 'September',
            'ru': 'Сентябрь',
        },
    },
    'September': {
        'rus': 'Сентябрь',
        'num': 9,
        'left': {
            'en': 'August',
            'ru': 'Август',
        },
        'right': {
            'en': 'October',
            'ru': 'Октябрь',
        },
    },
    'October': {
        'rus': 'Октябрь',
        'num': 10,
        'left': {
            'en': 'September',
            'ru': 'Сентябрь',
        },
        'right': {
            'en': 'November',
            'ru': 'Ноябрь',
        },
    },
    'November': {
        'rus': 'Ноябрь',
        'num': 11,
        'left': {
            'en': 'October',
            'ru': 'Октябрь',
        },
        'right': {
            'en': 'December',
            'ru': 'Декабрь',
        },
    },
    'December': {
        'rus': 'Декабрь',
        'num': 12,
        'left': {
            'en': 'November',
            'ru': 'Ноябрь',
        },
        'right': {
            'en': 'January',
            'ru': 'Январь',
        },
    },
}



MONTH_NUM = {
    1: {
        'rus': 'Январь',
        'in_text': 'января',
        'en': 'January',
    },
    2: {
        'rus': 'Февраль',
        'in_text': 'февраля',
        'en': 'February',
    },
    3: {
        'rus': 'Март',
        'in_text': 'марта',
        'en': 'March',
    },
    4: {
        'rus': 'Апрель',
        'in_text': 'апреля',
        'en': 'April',
    },
    5: {
        'rus': 'Май',
        'in_text': 'мая',
        'en': 'May',
    },
    6: {
        'rus': 'Июнь',
        'in_text': 'июня',
        'en': 'June',
    },
    7: {
        'rus': 'Июль',
        'in_text': 'июля',
        'en': 'July',
    },
    8: {
        'rus': 'Август',
        'in_text': 'августа',
        'en': 'August',
    },
    9: {
        'rus': 'Сентябрь',
        'in_text': 'сентября',
        'en': 'September',
    },
    10: {
        'rus': 'Октябрь',
        'in_text': 'октября',
        'en': 'October',
    },
    11: {
        'rus': 'Ноябрь',
        'in_text': 'ноября',
        'en': 'November',
    },
    12: {
        'rus': 'Декабрь',
        'in_text': 'декабря',
        'en': 'December',
    },
}