from aiogram import types
from aiogram.dispatcher import Dispatcher

from conversations.profile.utils import ProfileStates
from conversations.profile.keyboards import gender_markup, empty_markup, \
    start_markup
from conversations.profile.messages import MESSAGES

from main import dp


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(MESSAGES['greeting'],
                        reply_markup=start_markup, reply=False)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ProfileStates.all()[2])


@dp.message_handler(state=ProfileStates.GET_NAME)
async def ask_name(message: types.Message):
    await message.reply(MESSAGES['askname'], reply=False,
                        reply_markup=empty_markup)
    print(ProfileStates.all())
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ProfileStates.all()[4])


@dp.message_handler(state=ProfileStates.GET_SURNAME)
async def ask_surname(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(name=message.text)
    await message.reply(MESSAGES['asksurname'], reply=False)
    await state.set_state(ProfileStates.all()[1])


@dp.message_handler(state=ProfileStates.GET_GENDER)
async def ask_gender(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(surname=message.text)
    await message.reply(MESSAGES['askgender'], reply=False,
                        reply_markup=gender_markup)
    await state.set_state(ProfileStates.all()[0])


@dp.message_handler(state=ProfileStates.GET_AGE)
async def ask_age(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(gender=message.text)
    if message.text != "Мужской" and message.text != "Женский":
        await message.reply(MESSAGES['inputerror'])
        await state.set_state(ProfileStates.all()[0])
    else:
        await message.reply('Введите ваш возраст:', reply=False,
                            reply_markup=empty_markup)
        n = await state.get_data()
        print(n)
        await state.set_state(ProfileStates.all()[3])


@dp.message_handler(state=ProfileStates.GET_POSITION)
async def ask_position(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(age=message.text)
    try:
        age = int(message.text)
        if age < 1 or age > 150:
            raise ValueError
    except ValueError:
        await message.reply(MESSAGES['inputerror'])
        await state.set_state(ProfileStates.all()[3])
    else:
        await message.reply('', reply=False)


@dp.message_handler(state=ProfileStates.GET_POSITION)
async def ask_position(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(age=message.text)
    try:
        age = int(message.text)
        if age < 1 or age > 150:
            raise ValueError
    except ValueError:
        await message.reply(MESSAGES['inputerror'])
        await state.set_state(ProfileStates.all()[3])
    else:
        await message.reply(MESSAGES['askposition'], reply=False)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()