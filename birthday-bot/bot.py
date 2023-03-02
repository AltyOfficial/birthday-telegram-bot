import logging
import os
import time
import asyncio

import telegram
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters, CallbackQueryHandler)

import birthdays
import datetime
import messages
import calendar
import const
import utils

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

NAME, DATE = range(2)
name = ''
date = ''


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение от бота."""

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)

    await context.bot.send_sticker(
        chat_id=chat.id,
        sticker='CAADAgADOQADfyesDlKEqOOd72VKAg'
    )
    await context.bot.send_message(chat_id=chat.id, text=messages.GREETINGS)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Справка по использованию бота."""

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)

    await context.bot.send_message(chat_id=chat.id, text=messages.HELP)


# async def birthday_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Выводит список дней рождения по месяцам."""

#     try:
#         chat = update.effective_chat
#     except Exception as exc:
#         logging.error('Ошибка получения айди пользователя:', exc)
    

# async def show_month(update, context):
#     current_month = const.MONTH_NUM[datetime.date.today().month]['en']
#     data = const.MONTH[current_month]

    # keyboard = [
    #     [
    #         InlineKeyboardButton(
    #             '⬅️ ' + data['left']['ru'],
    #             callback_data=data['left']['en']
    #         ),
    #         InlineKeyboardButton(
    #             data['right']['ru'] + ' ➡️',
    #             callback_data=data['right']['en']
    #         ),
    #     ],
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)

    # await update.message.reply_text(
    #     text=utils.get_month_calendar(data['num']),
    #     parse_mode=telegram.constants.ParseMode.HTML,
    #     reply_markup=reply_markup
    # )


async def birthday_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводит список дней рождения по месяцам."""

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)
    
    current_month = const.MONTH_NUM[datetime.date.today().month]['en']
    data = const.MONTH[current_month]

    keyboard = [
        [
            InlineKeyboardButton(
                '⬅️ ' + data['left']['ru'],
                callback_data=data['left']['en']
            ),
            InlineKeyboardButton(
                data['right']['ru'] + ' ➡️',
                callback_data=data['right']['en']
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    items = await birthdays.get_birthday_list(chat.id, data['num'])
    response = ''

    for index, birthday in enumerate(items):
        response += f'{index + 1}. {birthday.name} - {birthday.date}\n'
    if response == '':
        response = 'Список дней рождения в этом месяце пуст.'

    text = utils.get_month_calendar(data['num']) + '\n' + response

    await update.message.reply_text(
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает сообщение и изменяет ответ."""

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)

    query = update.callback_query
    await query.answer()

    month = query.data
    data = const.MONTH[month]

    keyboard = [
        [
            InlineKeyboardButton(
                '⬅️ ' + data['left']['ru'],
                callback_data=data['left']['en']
            ),
            InlineKeyboardButton(
                data['right']['ru'] + ' ➡️',
                callback_data=data['right']['en']
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    items = await birthdays.get_birthday_list(chat.id, data['num'])
    response = ''

    for index, birthday in enumerate(items):
        response += f'{index + 1}. {birthday.name} - {birthday.date}\n'
    if response == '':
        response = 'Список дней рождения в этом месяце пуст.'

    text = utils.get_month_calendar(data['num']) + '\n' + response

    await query.edit_message_text(
        text=text,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=reply_markup
    )


async def add_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=messages.AddBirthday.ADD_NAME
    )
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global name
    name = update.message.text
    await update.message.reply_text(messages.AddBirthday.ADD_DATE)
    return DATE


async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global date
    chat_id = update.effective_chat.id
    date = update.message.text
    if date == 's':
        await context.bot.send_message(chat_id=chat_id, text='date')
        return DATE
    await context.bot.send_message(chat_id=chat_id, text=date)
    await update.message.reply_text(messages.AddBirthday.FINISH)
    await insert(update, context)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(messages.AddBirthday.CANCEL)
    return ConversationHandler.END


async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет информацию о дне рождения в базу данных."""
    global date

    date = date.strip()
    date = date.replace('/', '.')
    date = date.replace(' ', '.')

    logging.error('Ошибка получения айди пользователя:')

    chat_id = update.effective_chat.id
    await birthdays.add_bday(chat_id, name, date)


async def delete_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"""

    chat_id = update.effective_chat.id
    pass
    








if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    birthday_list_handler = CommandHandler('birthdays', birthday_list)
    application.add_handler(birthday_list_handler)
    application.add_handler(CallbackQueryHandler(button))

    bday_add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_birthday)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            DATE: [MessageHandler(filters.TEXT, date)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(bday_add_handler)

    
    application.run_polling()