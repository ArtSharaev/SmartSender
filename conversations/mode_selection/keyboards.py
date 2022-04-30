"""Несколько клавиатур"""

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

empty_markup = ReplyKeyboardRemove()

yes_btn = InlineKeyboardButton('Да', callback_data='yes_pressed')
no_btn = InlineKeyboardButton('Нет', callback_data='no_pressed')
ask_admin_markup = InlineKeyboardMarkup().row(yes_btn, no_btn)
