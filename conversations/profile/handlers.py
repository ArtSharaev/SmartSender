"""Машина состояний для составления анкеты"""

from aiogram import types

from conversations.profile.utils import ProfileStates
from conversations.profile.keyboards import gender_markup, empty_markup, \
    start_markup, position_markup
from conversations.profile.messages import MESSAGES
from conversations.user.keyboards import user_markup
from conversations.admin.keyboards import admin_markup

from main import dp

from data import db_session
from data.form_table import Form
from data.users_table import User

import datetime as dt


def check_not_user(user_id):
    db_sess = db_session.create_session()
    forms = db_sess.query(Form).all()
    for form in forms:
        if form.from_tg_user_id == user_id and form.status == 2:
            return False
    return True


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if check_not_user(message.from_user.id):
        await message.reply(MESSAGES['greeting'],
                            reply_markup=start_markup, reply=False)
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(ProfileStates.all()[2])
    else:
        db_sess = db_session.create_session()
        you = db_sess.query(User).filter(
            User.id == message.from_user.id).first()
        if you.privilege_level == 0:
            await message.reply(MESSAGES['have_form'],
                                reply_markup=user_markup, reply=False)
        else:
            await message.reply(MESSAGES['have_form'],
                                reply_markup=admin_markup, reply=False)


@dp.message_handler(state=ProfileStates.GET_NAME)
async def ask_name(message: types.Message):
    await message.reply(MESSAGES['askname'], reply=False,
                        reply_markup=empty_markup)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ProfileStates.all()[5])


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
        await message.reply(MESSAGES['askposition'], reply=False,
                            reply_markup=position_markup)
        await state.set_state(ProfileStates.all()[4])


@dp.message_handler(state=ProfileStates.GET_POSITION2)
async def ask_position2(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(position=message.text)
    if message.text != "Родитель" and message.text != "Ученик" and message.text != "Учитель":
        await message.reply(MESSAGES['inputerror'])
    else:
        d = await state.get_data()
        form = Form()
        form.from_tg_user_id = message.from_user.id
        form.created_date = dt.datetime.now()
        form.name = d["name"]
        form.surname = d["surname"]
        form.gender = d["gender"]
        form.age = d["age"]
        form.position = d["position"]
        form.status = 0
        form.changed_date = dt.datetime.now()
        db_sess = db_session.create_session()
        db_sess.add(form)
        db_sess.commit()
        await message.reply("Ваша анкета отправлена на модерацию!", reply=False,
                            reply_markup=empty_markup)
        await state.finish()
