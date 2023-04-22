import os
from dotenv import load_dotenv
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram import Update


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = """
Hello there!

Booking an auto now got simpler. Just send a message here to book an auto.

You can enter following commands:

/start - Display Main Menu
/book - Book an Auto
/about - About Us
/help - Get help for Booking
    """

    # print(menu_text)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text)


def main():
    print("Bot is running")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
