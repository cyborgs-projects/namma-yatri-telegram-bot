# import libraries
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# aiogram module
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


# keyboards.py
from keyboards import (
    MAIN_MENU_INLINE_KEYBOARD,
    VEHICLE_TYPE_KEYBOARD,
    PAYMENT_MODE_KEYBOARD,
    REMOVE_KEYBOARD,
)


# messages.py
from messages import (
    MSG_MAIN_MENU,
    MSG_HELP_MENU,
    MSG_BOOKING_CONFIRMED,
    MSG_BOOKING_STARTED,
    MSG_BOOKING_CANCELLED,
    MSG_FEATURE_COMING_SOON,
)


# database.py
from database import getUserBookingHistory, insertIntoDataBase, logIntoDataBase


# logger
logging.basicConfig(level=logging.INFO)


# bot token
load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")


# bot setup
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# states
class Form(StatesGroup):
    booking_time = State()
    pickup = State()
    destination = State()
    vehicle = State()
    payment = State()
    fare = State()

    name = State()
    age = State()
    gender = State()


# global variables
USER_ID = ""
USER_FULL_NAME = ""


# /start
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    global USER_ID, USER_FULL_NAME

    USER_ID = message.from_id
    USER_FULL_NAME = message.from_user.full_name
    LOG_ACTION = "chat started by user"

    now = datetime.now()
    curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

    logData = {
        "user_id": USER_ID,
        "user_full_name": USER_FULL_NAME,
        "action": LOG_ACTION,
        "createdAt": curr_time,
    }

    logIntoDataBase(logData)

    logging.info("%d - %s - %s", USER_ID, USER_FULL_NAME, LOG_ACTION)

    await message.reply(MSG_MAIN_MENU, reply_markup=MAIN_MENU_INLINE_KEYBOARD)


# /cancel
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == None:
        return

    USER_ID = message.from_id
    USER_FULL_NAME = message.from_user.full_name
    LOG_ACTION = "booking process cancelled by user from state"

    now = datetime.now()
    curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

    logData = {
        "user_id": USER_ID,
        "user_full_name": USER_FULL_NAME,
        "action": LOG_ACTION,
        "createdAt": curr_time,
    }

    logIntoDataBase(logData)

    logging.info(
        "%d - %s - %s - %r",
        USER_ID,
        USER_FULL_NAME,
        LOG_ACTION,
        current_state,
    )

    await message.reply(MSG_BOOKING_CANCELLED, reply_markup=MAIN_MENU_INLINE_KEYBOARD)

    await state.finish()


@dp.callback_query_handler(
    text=["book_ride", "booking_history", "settings", "get_help"]
)
async def main_menu_callback(call: types.CallbackQuery, state: FSMContext):
    global USER_ID, USER_FULL_NAME

    USER_ID = call.message.chat.id
    USER_FULL_NAME = ""

    # set USER_FULL_NAME
    if call.message.chat.first_name and call.message.chat.last_name:
        USER_FULL_NAME = (
            call.message.chat.first_name + " " + call.message.chat.last_name
        )
    elif call.message.chat.first_name:
        USER_FULL_NAME += call.message.chat.first_name
    elif call.message.chat.first_name:
        USER_FULL_NAME += call.message.chat.last_name

    # book_ride
    if call.data == "book_ride":
        now = datetime.now()
        curr_time = now.strftime("%d/%m/%Y %H:%M:%S")

        async with state.proxy() as data:
            data["booking_time"] = curr_time

        LOG_ACTION = "chat started by user"
        now = datetime.now()
        curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

        logData = {
            "user_id": USER_ID,
            "user_full_name": USER_FULL_NAME,
            "action": LOG_ACTION,
            "createdAt": curr_time,
        }

        logIntoDataBase(logData)

        logging.info("%d - %s - %s", USER_ID, USER_FULL_NAME, LOG_ACTION)

        await call.message.answer(MSG_BOOKING_STARTED, reply_markup=REMOVE_KEYBOARD)

        await Form.pickup.set()

    # booking_history
    if call.data == "booking_history":
        BOOKING_HISTORY = getUserBookingHistory(USER_ID)

        now = datetime.now()
        curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

        LOG_ACTION = "booking history viewed by user"

        logData = {
            "user_id": USER_ID,
            "user_full_name": USER_FULL_NAME,
            "action": LOG_ACTION,
            "createdAt": curr_time,
        }

        logIntoDataBase(logData)

        logging.info("%d - %s - %s", USER_ID, USER_FULL_NAME, LOG_ACTION)

        await call.message.answer(
            BOOKING_HISTORY, reply_markup=MAIN_MENU_INLINE_KEYBOARD
        )

    # settings
    if call.data == "settings":
        now = datetime.now()
        curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

        LOG_ACTION = "settings changed by user"

        logData = {
            "user_id": USER_ID,
            "user_full_name": USER_FULL_NAME,
            "action": LOG_ACTION,
            "createdAt": curr_time,
        }

        logIntoDataBase(logData)

        logging.info("%d - %s - %s", USER_ID, USER_FULL_NAME, LOG_ACTION)

        await call.message.answer(
            MSG_FEATURE_COMING_SOON, reply_markup=MAIN_MENU_INLINE_KEYBOARD
        )

    # get_help
    if call.data == "get_help":
        now = datetime.now()
        curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

        LOG_ACTION = "help taken by user"

        logData = {
            "user_id": USER_ID,
            "user_full_name": USER_FULL_NAME,
            "action": LOG_ACTION,
            "createdAt": curr_time,
        }

        logIntoDataBase(logData)

        logging.info("%d - %s - %s", USER_ID, USER_FULL_NAME, LOG_ACTION)

        await call.message.answer(MSG_HELP_MENU, reply_markup=MAIN_MENU_INLINE_KEYBOARD)

    await call.answer()


# pickup location
@dp.message_handler(state=Form.pickup, content_types=["location"])
async def pickup(message: types.Message, state: FSMContext):
    pickup_latitude = message.location.latitude
    pickup_longitude = message.location.longitude

    async with state.proxy() as data:
        data["pickup"] = [pickup_latitude, pickup_longitude]

    now = datetime.now()
    curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

    USER_ID = message.from_id
    USER_FULL_NAME = message.from_user.full_name
    LOG_ACTION = "user pickup location"

    logData = {
        "user_id": USER_ID,
        "user_full_name": USER_FULL_NAME,
        "action": LOG_ACTION,
        "pickup_latitude": pickup_latitude,
        "pickup_longitude": pickup_longitude,
        "createdAt": curr_time,
    }

    logIntoDataBase(logData)

    logging.info(
        "%d - %s - %s - latitute: %f - longitude: %f",
        USER_ID,
        USER_FULL_NAME,
        LOG_ACTION,
        pickup_latitude,
        pickup_longitude,
    )

    await message.answer("Great. Now send your destination")

    await Form.destination.set()


# destination location
@dp.message_handler(state=Form.destination, content_types=["location"])
async def destination(message: types.Message, state: FSMContext):
    destination_latitude = message.location.latitude
    destination_longitude = message.location.longitude

    async with state.proxy() as data:
        data["destination"] = [destination_latitude, destination_longitude]

    now = datetime.now()
    curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

    USER_ID = message.from_id
    USER_FULL_NAME = message.from_user.full_name
    LOG_ACTION = "user destination"

    logData = {
        "user_id": USER_ID,
        "user_full_name": USER_FULL_NAME,
        "action": LOG_ACTION,
        "destination_latitude": destination_latitude,
        "destination_longitude": destination_longitude,
        "createdAt": curr_time,
    }

    logIntoDataBase(logData)

    logging.info(
        "%d - %s - %s - latitute: %f - longitude: %f",
        USER_ID,
        USER_FULL_NAME,
        LOG_ACTION,
        destination_latitude,
        destination_longitude,
    )

    await message.answer("Select your vehicle type", reply_markup=VEHICLE_TYPE_KEYBOARD)

    await Form.vehicle.set()


# invalid input for vehicle type
@dp.message_handler(
    lambda message: message.text not in ["Auto", "Mini", "Sedan", "SUV"],
    state=Form.vehicle,
)
async def vehicle_invalid(message: types.Message):
    return await message.reply(
        "Invalid vehicle type. Choose your vehicle type from the keyboard."
    )


# vehicle type
@dp.message_handler(state=Form.vehicle)
async def vehicle(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        generated_fare = round(
            1000
            * (
                abs(data["pickup"][1] - data["destination"][1])
                + abs(data["pickup"][0] - data["destination"][0])
            ),
            2,
        )

        data["vehicle"] = message.text
        data["fare"] = generated_fare

    now = datetime.now()
    curr_time = now.strftime("%Y/%m/%d %H:%M:%S")


    vehicle_type=message.text
    USER_ID = message.from_id
    USER_FULL_NAME = message.from_user.full_name
    LOG_ACTION = "user vehicle type"

    logData = {
        "user_id": USER_ID,
        "user_full_name": USER_FULL_NAME,
        "action": LOG_ACTION,
        "vehicle_type": vehicle_type,
        "createdAt": curr_time,
    }

    logIntoDataBase(logData)

    logging.info(
        "%d - %s - %s - %s",
        message.from_id,
        message.from_user.full_name,
        LOG_ACTION,
        vehicle_type,
    )

    text = (
        "Your generated fare is Rs. " + str(generated_fare) + "\n\nSelect payment mode"
    )

    await message.answer(text, reply_markup=PAYMENT_MODE_KEYBOARD)

    await Form.payment.set()


# invalid input for payment mode
@dp.message_handler(
    lambda message: message.text not in ["Cash", "Online"], state=Form.payment
)
async def payment_invalid(message: types.Message):
    return await message.reply(
        "Invalid payment mode. Choose your payment mode from the keyboard."
    )


# payment mode
@dp.message_handler(state=Form.payment)
async def payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["payment"] = message.text

    now = datetime.now()
    curr_time = now.strftime("%Y/%m/%d %H:%M:%S")

    payment_mode= message.text
    LOG_ACTION="user payment mode"

    logData = {
        "user_id": USER_ID,
        "user_full_name": USER_FULL_NAME,
        "action": LOG_ACTION,
        "payment_mode": payment_mode,
        "createdAt": curr_time,
    }

    logIntoDataBase(logData)

    logging.info(
        "%d - %s - %s - %s",
        message.from_id,
        message.from_user.full_name,
        LOG_ACTION,
        payment_mode,
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
        + "\nPayment Mode: \t "
        + data["payment"]
        + "\nFare: \t "
        + str(data["fare"])
    )

    data = {
        "USER_ID": USER_ID,
        "USER_FULL_NAME": USER_FULL_NAME,
        "PICKUP_LATITUDE": data["pickup"][0],
        "PICKUP_LONGITUDE": data["pickup"][1],
        "DESTINATION_LATITUDE": data["destination"][0],
        "DESTINATION_LONGITUDE": data["destination"][1],
        "BOOKING_TIME": data["booking_time"],
        "VEHICLE_TYPE": data["vehicle"],
        "PAYMENT_MODE": data["payment"],
        "FARE": data["fare"],
    }

    insertIntoDataBase(data)

    await message.answer(BOOKING_SUMMARY, reply_markup=MAIN_MENU_INLINE_KEYBOARD)

    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
