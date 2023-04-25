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

import logging

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

SERVICE, DESTINATION, SOURCE, SETTINGS = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Book", "About", "Help"]]

    await update.message.reply_text(
        "Welcome to Yatri. How can we help you?: ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Select an option: "
        ),
    )

    return SERVICE

'''
async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected service and asks for destination location"""
    user = update.message.from_user
    logger.info("Requested service %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Now send destination location",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DESTINATION


async def destination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected destination and asks for pick-up location"""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of destination %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Great. Now share your pick up location"
    )

    return SOURCE


async def source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the source ans ends conversation"""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of destination %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Success"
    )

    return ConversationHandler.END
'''
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Different options (change language, phoneno)"""
    


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can travel again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6148407111:AAHPFuG0RNfK0OWqCtBOmLWvl01V2OCPv54").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SERVICE: [MessageHandler(filters.Regex("^(Book|About|Help)$"), service)],
            DESTINATION: [MessageHandler(filters.LOCATION, destination)],
            SOURCE: [MessageHandler(filters.LOCATION, source)],
            SETTINGS: [CommandHandler("settings", settings)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
