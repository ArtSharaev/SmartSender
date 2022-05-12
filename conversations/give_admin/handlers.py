"""Машина состояний для добавления админов"""

from aiogram import types

from conversations.give_admin.utils import GiveAdminStates
from conversations.give_admin.messages import MESSAGES
from conversations.give_admin.keyboards import ask_admin_markup
from conversations.admin.keyboards import admin_markup
from conversations.user.keyboards import user_markup

from data import db_session
from data.users_table import User

from main import dp, bot


@dp.message_handler(commands=['giveadmin'])
async def giveadmin_command(message: types.Message):
    if message.from_user.id == 5023078965:
        await bot.send_message(message.from_user.id, MESSAGES['ask_user'],
                               reply_markup=admin_markup)
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(GiveAdminStates.all()[0])


@dp.message_handler(state=GiveAdminStates.GIVE_ADMIN)
async def ask_admin(message: types.Message):
    if message.from_user.id == 5023078965:
        await bot.send_message(int(message.text), MESSAGES['give_admin'],
                               reply_markup=ask_admin_markup)
    state = dp.current_state(user=message.from_user.id)
    await state.finish()


@dp.callback_query_handler(text='yes_pressed')
async def pressed_yes(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id,
                           MESSAGES["admin_greeting"],
                           reply_markup=admin_markup)
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == callback_query.from_user.id).first()
    user.privilege_level = 1
    db_sess.commit()
    await bot.send_message(5023078965, f"{MESSAGES['greeting_notify']}"
                                       f" {str(callback_query.from_user.id)}",
                           reply_markup=admin_markup)


@dp.callback_query_handler(text='no_pressed')
async def pressed_no(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id,
                           MESSAGES["admin_negate"],
                           reply_markup=user_markup)
    await bot.send_message(5023078965, f"{MESSAGES['negate_notify']}"
                                       f" {str(callback_query.from_user.id)}",
                           reply_markup=admin_markup)

