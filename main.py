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

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)

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


async def sendSource(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = """
    Hi there! To help you find what you're looking for, can you please share your location with me? You can either type your address or share your current location by clicking on the paperclip icon and selecting "Location". Thank you!
    """
    # Create a keyboard with the "Share Location" button
    keyboard = KeyboardButton(text="Share Location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[keyboard]], resize_keyboard=True)

    # Create a keyboard with the "Share Location" button
    keyboard = KeyboardButton(text="Share Location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[keyboard]], resize_keyboard=True)

    # Send a message to the user with the keyboard
    update.message.reply_text(
        "Please share your location with me",
        reply_markup=reply_markup
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text)


def main():
    print("Bot is running")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    sourceLocation_handler = CommandHandler("sendSource", sendSource)
    application.add_handler(sourceLocation_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
