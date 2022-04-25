from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from main import dp


class ProfileStates(Helper):
    mode = HelperMode.snake_case

    GET_NAME = ListItem()
    GET_SURNAME = ListItem()
    GET_AGE = ListItem()
    GET_POSITION = ListItem()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('Заполнить анкету!'))
    await message.reply("Привет от разработчиков!\n\nЗаполните анкету,"
                        " чтобы получить доступ к функционалу.",
                        reply_markup=kb, reply=False)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ProfileStates.all()[1])


@dp.message_handler(lambda message: message.text == "Заполнить анкету!")
async def ask_name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ProfileStates.all()[1])


@dp.message_handler(state=ProfileStates.GET_NAME)
async def ask_name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.reply('Введите своё настоящее имя:', reply=False,
                        reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProfileStates.all()[2])


@dp.message_handler(state=ProfileStates.GET_SURNAME)
async def ask_surname(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(name=message.text)
    await message.reply('Введите свою настоящую фамилию:', reply=False)
    n = await state.get_data()
    print(n)
    await state.set_state(ProfileStates.all()[3])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()