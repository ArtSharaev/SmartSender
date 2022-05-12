"""Несколько клавиатур"""

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

empty_markup = ReplyKeyboardRemove()

send_btn = KeyboardButton("/send")
user_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(send_btn)

