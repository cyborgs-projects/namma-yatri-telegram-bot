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

(
    BOOK_CAB,
    DESTINATION,
    SOURCE,
    VEHICLE,
    PRICING,
    PAYMENT,
    VIEW_BOOKING_HISTORY,
    SETTINGS,
    GET_HELP,
) = range(9)


BOOKING_DETAILS = {}












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

    # user = update.message.from_user

    # logger.info("%s started chat", user.first_name)




    MSG_MAIN_MENU = """Welcome aboard! 🎉🚕🌟

At Namma Yatri 🚕, we believe that your journey should be as enjoyable as your destination. That's why we offer a hassle-free online cab booking experience that is safe, reliable and affordable. 💰💺

With our Telegram bot 🤖, you can book a ride in just a few clicks. Simply send us a message and our team of friendly bots will take care of the rest! 🤖🚗💨

Our experienced and courteous drivers will ensure that you reach your destination on time, every time. 🚕🌟 And with our comfortable, air-conditioned cabs, you can sit back, relax and enjoy the ride! 😎🚘

So why wait? Book your ride with Namma Yatri today and experience the joy of hassle-free travel! 🌟🌟🌟"""


    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MSG_MAIN_MENU,
        reply_markup=reply_markup,
    )

    


async def book_cab(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected service and asks for destination location"""

    '''
    Update(
        callback_query=CallbackQuery(
            chat_instance='-1377679089346078440',
            data='book_cab',
            from_user=User(
                first_name='Aditya',
                id=1697197699,
                is_bot=False,
                language_code='en',
                last_name='Thorat',
                username='thorataditya'
            ),
            id='7289408616126006785',
            message=Message(
                channel_chat_created=False,
                chat=Chat(
                    first_name='Aditya',
                    id=1697197699,
                    last_name='Thorat',
                    type=<ChatType.PRIVATE>,
                    username='thorataditya'
                ),
                date=datetime.datetime(2023, 4, 23, 11, 27, 59, tzinfo=<UTC>),
                delete_chat_photo=False,
                from_user=User(
                    first_name='testbot',
                    id=6154804837,
                    is_bot=True,
                    username='test20230419bot'
                ),
                group_chat_created=False,
                message_id=799,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=(
                        (
                            InlineKeyboardButton(
                                callback_data='book_cab',
                                text='Book a cab'
                            ),
                            InlineKeyboardButton(
                                callback_data='view_booking_history',
                                text='View booking history'
                            )
                        ),
                        (
                            InlineKeyboardButton(
                                callback_data='cancel_booking',
                                text='Cancel a booking'
                            ),
                            InlineKeyboardButton(
                                callback_data='get_help',
                                text='Get help'
                            )
                        )
                    )
                ),
                supergroup_chat_created=False,
                text="Welcome aboard! 🎉🚕🌟\n\nAt Namma Yatri 🚕, we believe that your journey should be as enjoyable as your destination. That's why we offer a hassle-free online cab booking experience that is safe, reliable and affordable. 💰💺\n\nWith our Telegram bot 🤖, you can book a ride in just a few clicks. Simply send us a message and our team of friendly bots will take care of the rest! 🤖🚗💨\n\nOur experienced and courteous drivers will ensure that you reach your destination on time, every time. 🚕🌟 And with our comfortable, air-conditioned cabs, you can sit back, relax and enjoy the ride! 😎🚘\n\nSo why wait? Book your ride with Namma Yatri today and experience the joy of hassle-free travel! 🌟🌟🌟"
            )
        ), update_id=720656082
    '''


    # user = update.message.from_user
    # logger.info("Requested service %s: %s", user.first_name, update.message.text)




    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Now send destination location",
    )

    return DESTINATION




async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")



'''
async def book_cab(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected service and asks for destination location"""
    
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Now send destination location"
    )

    return DESTINATION

'''






async def destination(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected destination and asks for pick-up location"""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of destination %s: %f / %f",
        user.first_name,
        user_location.latitude,
        user_location.longitude,
    )
    await update.message.reply_text("Great. Now share your pick up location")

    return SOURCE


async def source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the source ans ends conversation"""

    reply_keyboard = [["Auto", "Mini", "Sedan", "SUV"]]

    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of destination %s: %f / %f",
        user.first_name,
        user_location.latitude,
        user_location.longitude,
    )

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



async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("cancel")
    return ConversationHandler.END







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





async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Different options (change language, phoneno)"""
    



async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Need some help? 

No worries! Our 🤖bot is here to assist you. 
Simply type /help to see a list of available commands. 

If you need further assistance, feel free to reach out to our 📞customer support team at support@nammayatri.com or send us a message on our 📱social media channels. 

We're always happy to help!
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)




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

    # Add main handler

    # Add booking handler

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BOOK_CAB: [CommandHandler("book_cab", book_cab)],
            VIEW_BOOKING_HISTORY: [CommandHandler("view_booking_history", view_booking_history)],
            SETTINGS: [CommandHandler("settings", settings)],
            GET_HELP: [CommandHandler("get_help", get_help)],
            DESTINATION: [MessageHandler(filters.LOCATION, destination)],
            SOURCE: [MessageHandler(filters.LOCATION, source)],
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

    # booking_handler = ConversationHandler(
    #     entry_points=[CommandHandler("book_cab", book_cab,Update)],
    #     states={
            
    #     },
    #     fallbacks=[CommandHandler("cancel", cancel)],
    # )
    # application.add_handler(booking_handler)
    # callback
    # application.add_handler(CallbackQueryHandler(button))

    # application.add_handler(CallbackQueryHandler(book_cab, pattern="book_cab"))
    # application.add_handler(
    #     CallbackQueryHandler(view_booking_history, pattern="view_booking_history")
    # )
    # application.add_handler(
    #     CallbackQueryHandler(cancel_booking, pattern="cancel_booking")
    # )
    # application.add_handler(CallbackQueryHandler(get_help, pattern="get_help"))
    application.run_polling()


if __name__ == "__main__":
    main()
