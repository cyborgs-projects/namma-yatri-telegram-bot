import os
import logging
import sqlite3
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_TOKEN = os.environ.get("BOT_TOKEN")


import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# keyboard
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'

    booking_time = State()  # Will be represented in storage as 'Form:booking_time'
    destination = State()  # Will be represented in storage as 'Form:destination'
    pickup = State()  # Will be represented in storage as 'Form:pickup'
    vehicle = State()  # Will be represented in storage as 'Form:vehicle'
    payment = State()  # Will be represented in storage as 'Form:payment'
    fare = State()  # Will be represented in storage as 'Form:fare'


MSG_MAIN_MENU = """
Welcome aboard! 🎉🚕🌟

At Namma Yatri 🚕, we believe your journey should be as enjoyable as your destination. That's why we offer a hassle-free, safe and reliable online ride booking experience.

With our Telegram bot 🤖, you can book ride in just a few clicks. Simply send a message and our friendly bot will take care of the rest! 🤖🚗💨

Our experienced drivers will ensure that you reach your destination on time, always. 🚕🌟 So sit back comfortably, relax and enjoy your ride! 😎🚘
"""


MSG_HELP_MENU = """
Help menu

You can perform following actions:
1) Book a Ride
2) View Booking History
3) Change Settings
4) Get Help

Need more help? No worries! Our team is here to assist you.

If you need further assistance, feel free to reach out to our 📞 customer support team at support@nammayatri.com or send us a message on our 📱 social media channels. 

We're always happy to help!
"""
# 1) /book_ride - Book a Ride
# 2) /booking_history - View Booking History
# 3) /settings - Change Settings
# 4) /get_help - Get Help


MSG_BOOKING_CONFIRMED = """
Your booking has been Confirmed.

Enjoy your ride!
"""


MSG_NO_BOOKING_HISTORY = """
Oh no!

Looks like you haven't taken any rides with Namma Yatri yet.

What are you waiting for? Book your first ride now! 🚗💨
"""


MSG_BOOKING_STARTED = """
Ride booking process has started

Type /cancel or cancel anytime to stop booking process

Send your destination location
"""


main_menu_button1 = InlineKeyboardButton(text="Book a Ride", callback_data="book_ride")
main_menu_button2 = InlineKeyboardButton(
    text="Booking History", callback_data="booking_history"
)
main_menu_button3 = InlineKeyboardButton(
    text="Change Settings", callback_data="settings"
)
main_menu_button4 = InlineKeyboardButton(text="Get Help", callback_data="get_help")
MAIN_MENU_INLINE_KEYBOARD = (
    InlineKeyboardMarkup()
    .add(main_menu_button1, main_menu_button2)
    .add(main_menu_button3, main_menu_button4)
)


VEHICLE_TYPE_KEYBOARD = (
    ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    .add("Auto", "Mini")
    .add("Sedan", "SUV")
)


PAYMENT_MODE_KEYBOARD = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add("Cash", "Online")


REMOVE_KEYBOARD = ReplyKeyboardRemove()


USER_ID = ""
USER_FULL_NAME = ""


def createTableIfNotExists():
    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()
    c.execute(
        """
CREATE TABLE IF NOT EXISTS RIDE_HISTORY (
    RIDE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USER_ID INT NOT NULL,
    USER_FULL_NAME TEXT NOT NULL,
    PICKUP_LATITUDE REAL NOT NULL,
    PICKUP_LONGITUDE REAL NOT NULL,
    DESTINATION_LATITUDE REAL NOT NULL,
    DESTINATION_LONGITUDE REAL NOT NULL,
    BOOKING_TIME TEXT NOT NULL,
    VEHICLE_TYPE TEXT NOT NULL,
    PAYMENT_MODE TEXT NOT NULL,
    FARE INT NOT NULL
);
"""
    )
    conn.commit()
    conn.close()


def insertIntoDataBase(
    USER_ID,
    USER_FULL_NAME,
    PICKUP_LATITUDE,
    PICKUP_LONGITUDE,
    DESTINATION_LATITUDE,
    DESTINATION_LONGITUDE,
    BOOKING_TIME,
    VEHICLE_TYPE,
    PAYMENT_MODE,
    FARE,
):
    createTableIfNotExists()

    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()

    data = {
        "USER_ID": USER_ID,
        "USER_FULL_NAME": USER_FULL_NAME,
        "PICKUP_LATITUDE": PICKUP_LATITUDE,
        "PICKUP_LONGITUDE": PICKUP_LONGITUDE,
        "DESTINATION_LATITUDE": DESTINATION_LATITUDE,
        "DESTINATION_LONGITUDE": DESTINATION_LONGITUDE,
        "BOOKING_TIME": BOOKING_TIME,
        "VEHICLE_TYPE": VEHICLE_TYPE,
        "PAYMENT_MODE": PAYMENT_MODE,
        "FARE": FARE,
    }

    conn.execute(
        "INSERT INTO RIDE_HISTORY (USER_ID, USER_FULL_NAME, PICKUP_LATITUDE, PICKUP_LONGITUDE, DESTINATION_LATITUDE, DESTINATION_LONGITUDE, BOOKING_TIME, VEHICLE_TYPE, PAYMENT_MODE, FARE) VALUES (:USER_ID, :USER_FULL_NAME, :PICKUP_LATITUDE, :PICKUP_LONGITUDE, :DESTINATION_LATITUDE, :DESTINATION_LONGITUDE, :BOOKING_TIME, :VEHICLE_TYPE, :PAYMENT_MODE, :FARE)",
        data,
    )

    conn.commit()
    conn.close()


def getBookingHistory(USER_ID):
    createTableIfNotExists()

    conn = sqlite3.connect("ride_history.db")
    c = conn.cursor()
    c.execute("SELECT * FROM RIDE_HISTORY WHERE USER_ID=?", (USER_ID,))
    rides = c.fetchall()

    if not rides:
        return MSG_NO_BOOKING_HISTORY

    BOOKING_HISTORY = "Your ride history with Namma Yatri! 🚗💨\n"

    for i, ride in enumerate(rides):
        ride_number = i + 1

        BOOKING_HISTORY = BOOKING_HISTORY + (
            "\nRide Number: \t "
            + str(ride_number)
            + "\nBooking Time: \t "
            + str(ride[7])
            + "\nDestination: \n "
            + "\t\t\t\tlat: "
            + str(round(ride[5], 4))
            + "\t\t\t\tlong: "
            + str(round(ride[6], 4))
            + "\nPickup: \n "
            + "\t\t\t\tlat: "
            + str(round(ride[3], 4))
            + "\t\t\t\tlong: "
            + str(round(ride[4], 4))
            + "\nVehicle: \t "
            + str(ride[8])
            + "\nPayment Mode: \t "
            + str(ride[9])
            + "\nFare: \t "
            + str(ride[10])
            + "\n"
        )

    BOOKING_HISTORY += "\nThank you for choosing Namma Yatri! 😊"

    return BOOKING_HISTORY


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    global USER_ID
    USER_ID = message.from_id
    global USER_FULL_NAME
    USER_FULL_NAME = message.from_user.full_name

    logging.info("Chat started by user %d - %s", USER_ID, USER_FULL_NAME)

    await message.reply(MSG_MAIN_MENU, reply_markup=MAIN_MENU_INLINE_KEYBOARD)


@dp.callback_query_handler(
    text=["book_ride", "booking_history", "settings", "get_help", "cancel"]
)
async def main_menu_callback(call: types.CallbackQuery, state: FSMContext):
    global USER_ID
    USER_ID = call.message.chat.id
    global USER_FULL_NAME
    USER_FULL_NAME = ""

    if call.message.chat.first_name and call.message.chat.last_name:
        USER_FULL_NAME = (
            call.message.chat.first_name + " " + call.message.chat.last_name
        )
    elif call.message.chat.first_name:
        USER_FULL_NAME += call.message.chat.first_name
    elif call.message.chat.first_name:
        USER_FULL_NAME += call.message.chat.last_name

    if call.data == "book_ride":
        await Form.destination.set()

        now = datetime.now()
        curr_time = now.strftime("%d/%m/%Y %H:%M:%S")

        async with state.proxy() as data:
            data["booking_time"] = curr_time

        logging.info("Chat started by user %d - %s", USER_ID, USER_FULL_NAME)

        await call.message.answer(MSG_BOOKING_STARTED, reply_markup=REMOVE_KEYBOARD)
    if call.data == "booking_history":
        BOOKING_HISTORY = getBookingHistory(USER_ID)

        logging.info("Booking history viewed by user %d - %s", USER_ID, USER_FULL_NAME)

        await call.message.answer(
            BOOKING_HISTORY, reply_markup=MAIN_MENU_INLINE_KEYBOARD
        )

    if call.data == "settings":
        logging.info("Settings changed by user %d - %s", USER_ID, USER_FULL_NAME)

    if call.data == "get_help":
        logging.info("Help taken by user %d - %s", USER_ID, USER_FULL_NAME)

        await call.message.answer(MSG_HELP_MENU, reply_markup=MAIN_MENU_INLINE_KEYBOARD)

    if call.data == "cancel":
        print("cancel_button")

        current_state = await state.get_state()
        # if current_state is None:
        #     return

        logging.info(
            "Booking process cancelled by user %d - %s from state - %r",
            call.message.from_id,
            call.message.from_user.full_name,
            current_state,
        )

        await state.finish()
        await call.message.reply(
            "Booking process is cancelled", reply_markup=MAIN_MENU_INLINE_KEYBOARD
        )

    await call.answer()


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info(
        "Booking process cancelled by user %d - %s from state - %r",
        message.from_id,
        message.from_user.full_name,
        current_state,
    )

    await state.finish()
    await message.reply(
        "Booking process is cancelled", reply_markup=MAIN_MENU_INLINE_KEYBOARD
    )


@dp.message_handler(commands="book_ride")
async def book_ride(message: types.Message, state: FSMContext):
    await Form.destination.set()

    now = datetime.now()
    curr_time = now.strftime("%d/%m/%Y %H:%M:%S")

    async with state.proxy() as data:
        data["booking_time"] = curr_time

    logging.info(
        "Booking started by user %d - %s", message.from_id, message.from_user.full_name
    )

    await message.answer(MSG_BOOKING_STARTED)


@dp.message_handler(state=Form.destination)
async def destination(message: types.Message, state: FSMContext):
    destination_latitude = message.location.latitude
    destination_longitude = message.location.longitude

    async with state.proxy() as data:
        data["destination"] = [destination_latitude, destination_longitude]

    logging.info(
        "User %d - %s destination - latitute: %f - longitude: %f",
        message.from_id,
        message.from_user.full_name,
        destination_latitude,
        destination_longitude,
    )

    await Form.pickup.set()

    await message.answer("Great. Now send your pickup location")


@dp.message_handler(state=Form.pickup)
async def pickup(message: types.Message, state: FSMContext):
    pickup_latitude = message.location.latitude
    pickup_longitude = message.location.longitude

    async with state.proxy() as data:
        data["pickup"] = [pickup_latitude, pickup_longitude]

    logging.info(
        "User %d - %s pickup - latitute: %f - longitude: %f",
        message.from_id,
        message.from_user.full_name,
        pickup_latitude,
        pickup_longitude,
    )

    await Form.vehicle.set()
    await message.answer("Select your vehicle type", reply_markup=VEHICLE_TYPE_KEYBOARD)


@dp.message_handler(
    lambda message: message.text not in ["Auto", "Mini", "Sedan", "SUV"],
    state=Form.vehicle,
)
async def vehicle_invalid(message: types.Message):
    return await message.reply(
        "Invalid vehicle type. Choose your vehicle type from the keyboard."
    )


@dp.message_handler(state=Form.vehicle)
async def vehicle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["vehicle"] = message.text

    logging.info(
        "User %d - %s vehicle - %s",
        message.from_id,
        message.from_user.full_name,
        message.text,
    )

    await Form.next()

    await message.answer("Choose payment mode", reply_markup=PAYMENT_MODE_KEYBOARD)


@dp.message_handler(
    lambda message: message.text not in ["Cash", "Online"], state=Form.payment
)
async def payment_invalid(message: types.Message):
    return await message.reply(
        "Invalid payment option. Choose your payment option from the keyboard."
    )


@dp.message_handler(state=Form.payment)
async def payment(message: types.Message, state: FSMContext):
    # Update state and data
    async with state.proxy() as data:
        data["payment"] = message.text
        data["fare"] = 100

    logging.info(
        "User %d - %s payment - %s",
        message.from_id,
        message.from_user.full_name,
        message.text,
    )

    await message.answer(MSG_BOOKING_CONFIRMED, reply_markup=REMOVE_KEYBOARD)

    BOOKING_SUMMARY = (
        "Your booking summary\n"
        + "\nBooking Time: \t "
        + data["booking_time"]
        + "\nDestination: \n "
        + "\t\t\t\tlat: "
        + str(round(data["destination"][0], 4))
        + "\t\t\t\tlong: "
        + str(round(data["destination"][1], 4))
        + "\nPickup: \n "
        + "\t\t\t\tlat: "
        + str(round(data["pickup"][0], 4))
        + "\t\t\t\tlong: "
        + str(round(data["pickup"][1], 4))
        + "\nVehicle: \t "
        + data["vehicle"]
        + "\nPayment: \t "
        + data["payment"]
        + "\nFare: \t "
        + str(data["fare"])
    )

    PICKUP_LATITUDE = data["pickup"][0]
    PICKUP_LONGITUDE = data["pickup"][1]
    DESTINATION_LATITUDE = data["destination"][0]
    DESTINATION_LONGITUDE = data["destination"][1]
    BOOKING_TIME = data["booking_time"]
    VEHICLE_TYPE = data["vehicle"]
    PAYMENT_MODE = data["payment"]
    FARE = data["fare"]

    insertIntoDataBase(
        USER_ID,
        USER_FULL_NAME,
        PICKUP_LATITUDE,
        PICKUP_LONGITUDE,
        DESTINATION_LATITUDE,
        DESTINATION_LONGITUDE,
        BOOKING_TIME,
        VEHICLE_TYPE,
        PAYMENT_MODE,
        FARE,
    )

    await message.answer(BOOKING_SUMMARY, reply_markup=MAIN_MENU_INLINE_KEYBOARD)

    await state.finish()


@dp.message_handler(commands="booking_history")
async def booking_history(message: types.Message, state: FSMContext):
    global USER_ID
    USER_ID = message.from_id
    global USER_FULL_NAME
    USER_FULL_NAME = message.from_user.full_name

    logging.info("Booking history viewed by user %d - %s", USER_ID, USER_FULL_NAME)

    BOOKING_HISTORY = getBookingHistory(USER_ID)

    await message.reply(BOOKING_HISTORY, reply_markup=MAIN_MENU_INLINE_KEYBOARD)


@dp.message_handler(commands="get_help")
async def get_help(message: types.Message):
    global USER_ID
    USER_ID = message.from_id
    global USER_FULL_NAME
    USER_FULL_NAME = message.from_user.full_name

    logging.info("Help taken by user %d - %s", USER_ID, USER_FULL_NAME)

    await message.answer(MSG_HELP_MENU, reply_markup=MAIN_MENU_INLINE_KEYBOARD)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
