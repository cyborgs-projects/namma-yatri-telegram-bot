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


def isImported():
    print("book is imported")


async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = "Hello there!"
    # print(menu_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=menu_text)
