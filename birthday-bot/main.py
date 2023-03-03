import os
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, MessageHandler,
                          filters)
from dotenv import load_dotenv
import bot

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


# async def start(update, context):
#     await bot.start(update, context)


# async def help(update, context):
#     await bot.help(update, context)


# async def birthday_list(update, context):
#     await bot.birthday_list(update, context)


# async def button(update, context):
#     await bot.button(update, context)


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', bot.start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', bot.help)
    application.add_handler(help_handler)

    birthday_list_handler = CommandHandler('birthdays', bot.birthday_list)
    application.add_handler(birthday_list_handler)
    application.add_handler(CallbackQueryHandler(bot.button))

    bday_add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', bot.add_birthday)],
        states={
            bot.NAME: [MessageHandler(filters.TEXT, bot.name)],
            bot.DATE: [MessageHandler(filters.TEXT, bot.date)],
        },
        fallbacks=[CommandHandler('cancel', bot.cancel)],
    )
    application.add_handler(bday_add_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
