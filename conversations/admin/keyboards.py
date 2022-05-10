"""Несколько клавиатур"""

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

empty_markup = ReplyKeyboardRemove()

accept_btn = InlineKeyboardButton('Принять ✅', callback_data='accept_form')
reject_btn = InlineKeyboardButton('Отклонить ❌', callback_data='reject_form')
form_markup = InlineKeyboardMarkup().row(reject_btn, accept_btn)
