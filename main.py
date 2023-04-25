'''
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import Update, ReplyKeyboardMarkup



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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    book.book()


async def get_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?",
        ),
    )


def main():
    print("Bot is running")

    book.isImported()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    book_handler = CommandHandler("book", book.book)
    application.add_handler(book_handler)

    application.run_polling()


if __name__ == "__main__":
    main()

'''


#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging

from dotenv import load_dotenv

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

(
    VEHICLE,
    PRICING,
    CONFIRM,
    PAYMENT,
) = range(4)


load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


BOOKING_DETAILS = {}


'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their vehicle."""
    reply_keyboard = [["Auto", "Mini", "Sedan", "SUV"]]

    user = update.message.from_user

    logger.info("%s started chat", user.first_name)

    await update.message.reply_text(
        "Hi!" "Send /cancel to stop booking.\n\n" "Select vehicle to book.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Auto, Mini, Sedan or SUV?",
        ),
    )

    return VEHICLE


async def vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Select vehicle type."""
    reply_keyboard = [["Proceed", "Cancel"]]

    user = update.message.from_user
    logger.info("%s vehicle: %s", user.first_name, update.message.text)

    BOOKING_DETAILS[vehicle] = update.message.text

    await update.message.reply_text(
        "Your total amount will be: Rs. 100",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Proceed or Cancel",
        ),
    )

    return PRICING


async def pricing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show amount and booking details."""
    reply_keyboard = [["Cash", "Online"]]

    user = update.message.from_user
    logger.info("%s pricing: %s", user.first_name, update.message.text)

    USER_DECISION = update.message.text

    if (USER_DECISION) == "Proceed":
        await update.message.reply_text(
            "select payment mode.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                input_field_placeholder="Cash or Online",
            ),
        )
        return PAYMENT

    elif (USER_DECISION) == "Cancel":
        print("in Cancel")
        # CommandHandler("cancel", cancel)

        # return ConversationHandler.END
        # return CONFIRM


async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Select payment mode."""

    user = update.message.from_user
    # photo_file = await update.message.photo[-1].get_file()
    # await photo_file.download_to_drive("user_photo.jpg")
    logger.info("%s payment: %s", user.first_name, update.message.text)

    selected_payment_mode = update.message.text

    # print(selected_payment_mode)
    # print(selected_payment_mode.lower() == "online")
    # print(selected_payment_mode.lower() == "Cash")

    if (selected_payment_mode) == "Online":
        print("Online payment selected.")
        await update.message.reply_text(
            "Online payment selected.",
            reply_markup=ReplyKeyboardRemove(),
        )

    elif (selected_payment_mode) == "Cash":
        print("Cash payment selected.")

        OUTPUT_TEXT = """
You have selected Cash mode. Pay the driver once you reach your destination.
"""

        await update.message.reply_text(
            OUTPUT_TEXT,
            reply_markup=ReplyKeyboardRemove(),
        )

'''




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            VEHICLE: [
                MessageHandler(filters.Regex("^(Auto|Mini|Sedan|SUV)$"), vehicle)
            ],
            PRICING: [
                MessageHandler(filters.Regex("^(Proceed|Cancel)$"), pricing),
            ],
            PAYMENT: [
                MessageHandler(filters.Regex("^(Cash|Online)$"), payment),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
