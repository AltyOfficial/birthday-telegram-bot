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
JANUARY = range(1)
MONTH = range(1)
ROUTES = range(1)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение от бота."""
    # keyboard = [
    #     [
    #         InlineKeyboardButton('1', callback_data='11111'),
    #         InlineKeyboardButton('2', callback_data='22222'),
    #     ]
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)

    await context.bot.send_sticker(
        chat_id=chat.id,
        sticker='CAADAgADOQADfyesDlKEqOOd72VKAg'
    )
    await context.bot.send_message(chat_id=chat.id, text=messages.GREETINGS)
    # await update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)

    # month = calendar.month(2023, 2)
    # today = str(datetime.date.today().day)
    # month = month.replace(f'{today}', f'</code><u>{today}</u><code>')
    # text = f'<code>{month}</code>'
    # await context.bot.send_message(
    #     chat_id=chat.id,
    #     text=text,
    #     parse_mode=telegram.constants.ParseMode.HTML
    # )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=messages.HELP)


async def bday_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    items = await birthdays.get_bday_list(chat_id)
    response = ''
    for index, birthday in enumerate(items):
        response += f'{index + 1}. {birthday.name} - {birthday.date}\n'
    if response == '':
        response = 'Вы не добавили ни одного дня рождения'
    await context.bot.send_message(chat_id=chat_id, text=response)


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
    





async def show_month(update, context):
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

    await update.message.reply_text(
        text=utils.get_month_calendar(data['num']),
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""

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

    await query.edit_message_text(
        text=utils.get_month_calendar(data['num']),
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=reply_markup
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    bday_list_handler = CommandHandler('list', bday_list)
    application.add_handler(bday_list_handler)

    bday_add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_birthday)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            DATE: [MessageHandler(filters.TEXT, date)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(bday_add_handler)

    conv_handler = CommandHandler('month', show_month)
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button))

    
    application.run_polling()