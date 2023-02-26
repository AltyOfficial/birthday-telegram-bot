import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)

import birthdays
import messages

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

NAME, DATE = range(2)
name = ''
date = ''


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_sticker(chat_id=chat_id, sticker='CAADAgADOQADfyesDlKEqOOd72VKAg')
    await context.bot.send_message(chat_id=chat_id, text=messages.GREETINGS)


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


async def add_bday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=messages.ADD)
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global name
    chat_id = update.effective_chat.id
    name = update.message.text
    await update.message.reply_text("Next is date.")
    return DATE

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global date
    chat_id = update.effective_chat.id
    date = update.message.text
    await context.bot.send_message(chat_id=chat_id, text=date)
    await update.message.reply_text("Thanks.")
    await insert(update, context)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    await update.message.reply_text(
        "Bye! I hope we can talk again some day."
    )

    return ConversationHandler.END

async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await birthdays.add_bday(chat_id, name, date)
    await context.bot.send_message(chat_id=chat_id, text='Готово!')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    bday_list_handler = CommandHandler('list', bday_list)
    application.add_handler(bday_list_handler)

    bday_add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_bday)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            DATE: [MessageHandler(filters.TEXT, date)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(bday_add_handler)
    
    application.run_polling()