"""Несколько клавиатур"""

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

empty_markup = ReplyKeyboardRemove()

user_btn = InlineKeyboardButton('Пользователь', callback_data='user')
admin_btn = InlineKeyboardButton('Администратор', callback_data='admin')
select_mode_markup = InlineKeyboardMarkup().row(user_btn, admin_btn)
