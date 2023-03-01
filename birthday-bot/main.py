# import os
# from telegram.ext import ApplicationBuilder, CommandHandler
# from dotenv import load_dotenv
# import bot

# load_dotenv()

# TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


# async def start(update, context):
#     await bot.start(update, context)


# async def help(update, context):
#     await bot.help(update, context)


# def main():
#     application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

#     start_handler = CommandHandler('start', start)
#     application.add_handler(start_handler)

#     application.run_polling()


# if __name__ == '__main__':
#     main()
