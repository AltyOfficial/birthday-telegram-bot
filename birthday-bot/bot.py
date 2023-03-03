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


async def birthday_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводит список дней рождения по месяцам."""

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)
    
    current_month = const.MONTH_NUM[datetime.date.today().month]['en']
    month_data = const.MONTH[current_month]

    keyboard = utils.make_calendar_keyboard(month_data)
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = await utils.make_response(chat.id, month_data['num'])

    await update.message.reply_text(
        text=message,
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

    month_data = const.MONTH[query.data]

    keyboard = utils.make_calendar_keyboard(month_data)
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = await utils.make_response(chat.id, month_data['num'])

    await query.edit_message_text(
        text=message,
        parse_mode=telegram.constants.ParseMode.HTML,
        reply_markup=reply_markup
    )


async def add_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет день рождения."""

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)

    await context.bot.send_message(
        chat_id=chat.id,
        text=messages.AddBirthday.ADD_NAME
    )

    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает информацию о человеке."""

    global name
    name = update.message.text

    if name == '/cancel':
        await update.message.reply_text(messages.AddBirthday.CANCEL)
        return ConversationHandler.END

    if len(name) > 50:
        await update.message.reply_text(messages.AddBirthday.ERROR_NAME)
        return ConversationHandler.NAME

    await update.message.reply_text(
        messages.AddBirthday.ADD_DATE,
        parse_mode=telegram.constants.ParseMode.HTML,
    )

    return DATE


async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает дату рождения человека."""

    global date
    date = update.message.text
    date = date.strip()
    date = date.replace('/', '.')
    date = date.replace(' ', '.')

    if date == '/cancel':
        await update.message.reply_text(messages.AddBirthday.CANCEL)
        return ConversationHandler.END

    try:
        datetime.datetime.strptime(date, "%d.%m.%Y")
    except Exception:
        await update.message.reply_text(
            messages.AddBirthday.ERROR_DATE,
            parse_mode=telegram.constants.ParseMode.HTML,
        )
        return DATE

    year = int(date[6:])
    current_year = datetime.date.today().year

    if not current_year - 150 < year < current_year + 150  or len(date) != 10:
        await update.message.reply_text(
            messages.AddBirthday.ERROR_DATE,
            parse_mode=telegram.constants.ParseMode.HTML,
        )
        return DATE

    await update.message.reply_text(messages.AddBirthday.FINISH)

    await insert(update, context)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет и заканчивает создание дня рождения."""

    await update.message.reply_text(messages.AddBirthday.CANCEL)

    return ConversationHandler.END


async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет информацию о дне рождения в базу данных."""

    global date

    try:
        chat = update.effective_chat
    except Exception as exc:
        logging.error('Ошибка получения айди пользователя:', exc)

    await birthdays.add_bday(chat.id, name, date)


async def delete_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """"""

    chat_id = update.effective_chat.id
    pass
