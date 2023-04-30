from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_menu_button1 = InlineKeyboardButton(text="Book a Ride", callback_data="book_ride")
main_menu_button2 = InlineKeyboardButton(text="Booking History", callback_data="booking_history")
main_menu_button3 = InlineKeyboardButton(text="Change Settings", callback_data="settings")
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
