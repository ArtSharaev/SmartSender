from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

empty_markup = ReplyKeyboardRemove()

start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_markup.add(KeyboardButton('Заполнить анкету!'))

female_btn = KeyboardButton('Женский')
male_btn = KeyboardButton('Мужской')
gender_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                    one_time_keyboard=True
                                    ).row(female_btn, male_btn)
