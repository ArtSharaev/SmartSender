"""Несколько клавиатур"""

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

empty_markup = ReplyKeyboardRemove()

accept_btn = InlineKeyboardButton('Принять ✅', callback_data='accept_form')
reject_btn = InlineKeyboardButton('Отклонить ❌', callback_data='reject_form')
form_markup = InlineKeyboardMarkup().row(reject_btn, accept_btn)

start_btn = KeyboardButton("/start")
start_markup = ReplyKeyboardMarkup().row(start_btn)


send_btn = KeyboardButton("/send")
getform_btn = KeyboardButton("/getform")
admin_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(send_btn,
                                                             getform_btn)

