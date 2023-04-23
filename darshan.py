import logging
import os
from dotenv import load_dotenv
import sqlite3
from telegram import (
    __version__ as TG_VER,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
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


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, BOOK_CAB, PHOTO, LOCATION, BIO = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Book a cab", callback_data="book_cab"),
            InlineKeyboardButton(
                "View booking history", callback_data="view_booking_history"
            ),
        ],
        [
            InlineKeyboardButton("Cancel a booking", callback_data="cancel_booking"),
            InlineKeyboardButton("Get help", callback_data="get_help"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        """Welcome aboard! 🎉🚕🌟

At Namma Yatri 🚕, we believe that your journey should be as enjoyable as your destination. That's why we offer a hassle-free online cab booking experience that is safe, reliable and affordable. 💰💺

With our Telegram bot 🤖, you can book a ride in just a few clicks. Simply send us a message and our team of friendly bots will take care of the rest! 🤖🚗💨

Our experienced and courteous drivers will ensure that you reach your destination on time, every time. 🚕🌟 And with our comfortable, air-conditioned cabs, you can sit back, relax and enjoy the ride! 😎🚘

So why wait? Book your ride with Namma Yatri today and experience the joy of hassle-free travel! 🌟🌟🌟""",
        reply_markup=reply_markup,
    )

    return CHOOSING


def defineTable():

    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS RIDE_HISTORY
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  USER_ID INT NOT NULL,
                  PICKUP_LOCATION TEXT NOT NULL,
                  DROP_LOCATION TEXT NOT NULL,
                  RIDE_DATE TEXT NOT NULL,
                  FARE INT NOT NULL);"""
    )
    conn.commit()
    conn.close()


def updateDataBase(user_id, pickup_location, drop_location, ride_date, fare):
    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS RIDE_HISTORY
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                  USER_ID INT NOT NULL,
                  PICKUP_LOCATION TEXT NOT NULL,
                  DROP_LOCATION TEXT NOT NULL,
                  RIDE_DATE TEXT NOT NULL,
                  FARE INT NOT NULL);"""
    )
    data = {
        "user_id": user_id,
        "pickup_location": pickup_location,
        "drop_location": drop_location,
        "ride_date": ride_date,
        "fare": fare,
    }

    conn.execute(
        "INSERT INTO RIDE_HISTORY (USER_ID, PICKUP_LOCATION, DROP_LOCATION, RIDE_DATE, FARE) \
              VALUES (:user_id, :pickup_location, :drop_location, :ride_date, :fare)",
        data,
    )

    conn.commit()
    conn.close()


async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
Need some help? 

No worries! Our 🤖bot is here to assist you. 
Simply type /help to see a list of available commands. 

If you need further assistance, feel free to reach out to our 📞customer support team at support@nammayatri.com or send us a message on our 📱social media channels. 

We're always happy to help!
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


async def view_booking_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user: User = update.message.from_user
    user = update.effective_user
    userID = user.username
    # print(userID)
    defineTable()
    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()
    c.execute("SELECT * FROM RIDE_HISTORY WHERE USER_ID=?", (userID,))
    rides = c.fetchall()

    if not rides:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="""Oh no! Looks like you haven't taken any rides with Namma Yatri yet. What are you waiting for? Book a ride now! 🚗💨""",
        )
        return

    output_message = "Here's your ride history with Namma Yatri! 🚗💨\n\n"

    for i, ride in enumerate(rides):
        ride_number = i + 1
        pickup_location = ride[2]
        drop_location = ride[3]
        ride_date = ride[4]
        fare = ride[5]

        output_message += f"Ride #{ride_number}:\n"
        output_message += f"Pickup location: {pickup_location}\n"
        output_message += f"Drop location: {drop_location}\n"
        output_message += f"Ride date: {ride_date}\n"
        output_message += f"Fare: ${fare}\n\n"

    output_message += "Thank you for choosing Namma Yatri! 😊"

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=output_message
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )
    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f",
        user.first_name,
        user_location.latitude,
        user_location.longitude,
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )
    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )
    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def book_cab(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("booking")

    return ConversationHandler.END


async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("cancel")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [],
            BOOK_CAB: [CommandHandler("book_cab", book_cab)],
            PHOTO: [
                MessageHandler(filters.PHOTO, photo),
                CommandHandler("skip", skip_photo),
            ],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    application.add_handler(CallbackQueryHandler(book_cab, pattern="book_cab"))

    application.add_handler(
        CallbackQueryHandler(view_booking_history, pattern="view_booking_history")
    )
    application.add_handler(
        CallbackQueryHandler(cancel_booking, pattern="cancel_booking")
    )
    application.add_handler(CallbackQueryHandler(get_help, pattern="get_help"))
    application.run_polling()


if __name__ == "__main__":
    main()
