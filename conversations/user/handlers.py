"""Машина состояний для составления анкеты"""

from aiogram import types

from conversations.user.utils import UserStates
from conversations.user.messages import MESSAGES
from conversations.user.keyboards import user_markup, empty_markup
from conversations.admin.keyboards import admin_markup
from conversations.profile.keyboards import position_markup

from main import dp, bot

from data import db_session
from data.form_table import Form
from data.users_table import User


def check_user(user_id):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.id == user_id).first():
        return True
    return False


@dp.message_handler(commands=['send'])
async def send_command(message: types.Message):
    if check_user(message.from_user.id):
        await bot.send_message(message.from_user.id, MESSAGES['get_recipient'],
                               reply_markup=position_markup)
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(UserStates.all()[1])


@dp.message_handler(state=UserStates.GET_RECIPIENT)
async def get_recipient(message: types.Message):
    if message.text != "Родитель" and message.text != "Ученик" and message.text != "Учитель":
        await message.reply(MESSAGES['inputerror'])
    else:
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(recipient=message.text)
        await bot.send_message(message.from_user.id, MESSAGES['get_message'],
                               reply_markup=empty_markup)
        await state.set_state(UserStates.all()[0])


@dp.message_handler(state=UserStates.GET_MESSAGE)
async def get_recipient(message: types.Message):
    db_sess = db_session.create_session()
    state = dp.current_state(user=message.from_user.id)
    you = db_sess.query(User).filter(User.id == message.from_user.id).first()
    name = you.name
    surname = you.surname
    position = you.position
    d = await state.get_data()
    count = 0
    for user in db_sess.query(User).filter(
            User.position == d["recipient"],
            User.id != message.from_user.id).all():
        count += 1
        await bot.send_message(
            user.id,
            f"Сообщение от {name} {surname}, {position.lower()}:\n {message.text}")
    if you.privilege_level == 0:
        await bot.send_message(
            message.from_user.id,
            f"Ваше сообщение отправлено {str(count)} пользователям.",
            reply_markup=user_markup)
    else:
        await bot.send_message(
            message.from_user.id,
            f"Ваше сообщение отправлено {str(count)} пользователям.",
            reply_markup=admin_markup)
    await state.finish()
