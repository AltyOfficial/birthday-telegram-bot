import os
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from dotenv import load_dotenv
import bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


async def start(update, context):
    await bot.start(update, context)


async def help(update, context):
    await bot.help(update, context)


async def birthday_list(update, context):
    await bot.birthday_list(update, context)


async def button(update, context):
    await bot.button(update, context)


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    birthday_list_handler = CommandHandler('birthdays', birthday_list)
    application.add_handler(birthday_list_handler)
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


if __name__ == '__main__':
    main()
