from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from conversations.profile.utils import ProfileStates
from main import dp


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('Заполнить анкету!'))
    await message.reply("Привет от разработчиков!\n\nЗаполните анкету,"
                        " чтобы получить доступ к функционалу.",
                        reply_markup=kb, reply=False)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ProfileStates.all()[2])


@dp.message_handler(state=ProfileStates.GET_NAME)
async def ask_name(message: types.Message):
    await message.reply('Начнём составление анкеты.\n', reply=False,
                        reply_markup=ReplyKeyboardRemove())
    await message.reply('Введите своё настоящее имя:', reply=False)
    print(ProfileStates.all())
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ProfileStates.all()[4])


@dp.message_handler(state=ProfileStates.GET_SURNAME)
async def ask_surname(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(name=message.text)
    await message.reply('Введите свою настоящую фамилию:', reply=False)
    await state.set_state(ProfileStates.all()[1])


@dp.message_handler(state=ProfileStates.GET_GENDER)
async def ask_surname(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(surname=message.text)
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
        KeyboardButton('Женский'), KeyboardButton('Мужской')
    )
    await message.reply('Выберите ваш пол:', reply=False, reply_markup=kb)
    await state.set_state(ProfileStates.all()[0])


@dp.message_handler(state=ProfileStates.GET_AGE)
async def ask_surname(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(gender=message.text)
    if message.text != "Мужской" and message.text != "Женский":
        await message.reply('Ошибка ввода. Попробуйте еще раз.')
        await state.set_state(ProfileStates.all()[0])
    else:
        await message.reply('Введите ваш возраст:', reply=False,
                            reply_markup=ReplyKeyboardRemove())
        n = await state.get_data()
        print(n)
        await state.set_state(ProfileStates.all()[3])


@dp.message_handler(state=ProfileStates.GET_POSITION)
async def ask_surname(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(age=message.text)
    await message.reply('Выберите свою должность:', reply=False)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()