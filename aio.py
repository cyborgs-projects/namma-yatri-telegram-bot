import os
import logging
from dotenv import load_dotenv

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
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    book_cab = State()  # Will be represented in storage as 'Form:book_cab'
    name = State()  # Will be represented in storage as 'Form:name'
    age = State()  # Will be represented in storage as 'Form:age'
    gender = State()  # Will be represented in storage as 'Form:gender'
    destination = State()  # Will be represented in storage as 'Form:destination'
    pickup = State()  # Will be represented in storage as 'Form:pickup'
    vehicle = State()  # Will be represented in storage as 'Form:vehicle'
    payment = State()  # Will be represented in storage as 'Form:payment'





keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("👋 Hello!", "💋 Youtube")





@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """

    button1 = InlineKeyboardButton(text="Book a cab", callback_data="book_cab")
    button2 = InlineKeyboardButton(text="View booking history", callback_data="view_booking_history")
    button3 = InlineKeyboardButton(text="Cancel a booking", callback_data="settings")
    button4 = InlineKeyboardButton(text="Get help", callback_data="get_help")
    keyboard_inline = InlineKeyboardMarkup().add(button1, button2).add(button3, button4)



    MSG_MAIN_MENU = """Welcome aboard! 🎉🚕🌟

At Namma Yatri 🚕, we believe that your journey should be as enjoyable as your destination. That's why we offer a hassle-free online cab booking experience that is safe, reliable and affordable. 💰💺

With our Telegram bot 🤖, you can book a ride in just a few clicks. Simply send us a message and our team of friendly bots will take care of the rest! 🤖🚗💨

Our experienced and courteous drivers will ensure that you reach your destination on time, every time. 🚕🌟 And with our comfortable, air-conditioned cabs, you can sit back, relax and enjoy the ride! 😎🚘

So why wait? Book your ride with Namma Yatri today and experience the joy of hassle-free travel! 🌟🌟🌟"""



    await message.reply(MSG_MAIN_MENU, reply_markup=keyboard_inline)










@dp.callback_query_handler(text=["book_cab", "view_booking_history", "settings", "get_help"])
async def start_call_back(call: types.CallbackQuery):
    
    if(call.data=="book_cab"):
        # Set state
        await Form.book_cab.set()

        await call.message.answer("Booking your cab")

        # await call.message.answer(call.message.chat.id)
        await call.answer()

    run_command(call.message.chat.id, call.data)


async def run_command(chat_id, selected_command):
    command = "/" + str(selected_command)
    await bot.send_message(chat_id, command)




















@dp.message_handler(state=Form.book_cab)
@dp.message_handler(commands="book_cab")
async def book_cab(message: types.Message):
    # Set state
    await Form.next()

    await message.answer("Enter your destination")


@dp.message_handler(state=Form.destination)
async def destination(message: types.Message, state: FSMContext):
    """
    Process user destination
    """
    async with state.proxy() as data:
        data['destination'] = message.text

    await Form.next()
    await message.answer("Great. Now share your pick up location")







@dp.message_handler(state=Form.pickup)
async def pickup(message: types.Message, state: FSMContext):
    """
    Process user destination
    """
    # Configure ReplyKeyboardMarkup
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    reply_keyboard.add("Auto", "Mini")
    reply_keyboard.add("Sedan", "SUV")





    async with state.proxy() as data:
        data['pickup'] = message.text

    await Form.next()
    await message.answer("Select your vehicle tyoe", reply_markup=reply_keyboard)





@dp.message_handler(lambda message: message.text not in ["Auto", "Mini", "Sedan", "SUV"], state=Form.vehicle)
async def vehicle_invalid(message: types.Message):
    return await message.reply("Bad vehicle type. Choose your vehicle type from the keyboard.")


@dp.message_handler(state=Form.vehicle)
async def vehicle(message: types.Message, state: FSMContext):
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    reply_keyboard.add("Cash", "Online")

    # Update state and data
    async with state.proxy() as data:
        data['vehicle'] = message.text


    await Form.next()

    await message.answer("Choose payment mode", reply_markup=reply_keyboard)













@dp.message_handler(lambda message: message.text not in ["Auto", "Mini", "Sedan", "SUV"], state=Form.vehicle)
async def payment_invalid(message: types.Message):
    return await message.reply("Bad vehicle type. Choose your gender from the keyboard.")


@dp.message_handler(state=Form.payment)
async def payment(message: types.Message, state: FSMContext):


    # Update state and data
    async with state.proxy() as data:
        data['payment'] = message.text


    # await Form.next()


    remove_keyboard = ReplyKeyboardRemove()

    USER_DATA = "Destination: \t " + data["destination"] + "\n" \
    + "Pickup: \t " + data["pickup"] + "\n" \
    + "Vehicle: \t " + data["vehicle"] + "\n" \
    + "Payment: \t " + data["payment"] + "\n"
    
    await message.answer(USER_DATA, reply_markup=remove_keyboard)


    await state.finish()




# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply("Cancelled.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data["name"] = message.text

    await Form.next()
    await message.reply("How old are you?")


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("Age gotta be a number.\nHow old are you? (digits only)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(age=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Male", "Female")
    markup.add("Other")

    await message.reply("What is your gender?", reply_markup=markup)


@dp.message_handler(
    lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender
)
async def process_gender_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Bad gender name. Choose your gender from the keyboard.")


@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["gender"] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # And send message
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text("Hi! Nice to meet you,", md.bold(data["name"])),
                md.text("Age:", md.code(data["age"])),
                md.text("Gender:", data["gender"]),
                sep="\n",
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    # Finish conversation
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
