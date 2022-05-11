"""Машина состояний для работы админа"""

from aiogram import types

from conversations.admin.keyboards import form_markup, empty_markup
from conversations.admin.utils import AdminStates
from conversations.admin.messages import MESSAGES

from main import dp, bot

from data import db_session
from data.form_table import Form
from data.users_table import User


@dp.message_handler(commands=['getform'])
async def getform_command(message: types.Message):
    db_sess = db_session.create_session()
    if ((message.from_user.id == 5023078965) or
            (message.from_user.id in db_sess.query(User).filter(
                User.privilege_level == 1))):
        form = db_sess.query(Form).first()
        msg = f"""
          Анкета номер {str(form.id)}:
        Создана {str(form.created_date)}
        {form.name} {form.surname}
        Возраст: {str(form.age)}
        Пол: {form.gender}
        {form.position}
        """
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(form_user_id=form.from_tg_user_id)
        await bot.send_message(message.from_user.id, msg,
                               reply_markup=form_markup)


@dp.callback_query_handler(text='accept_form')
async def form_accepted(callback_query: types.CallbackQuery):
    await callback_query.answer(text="ok",
                                show_alert=True)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)


@dp.callback_query_handler(text='reject_form')
async def form_rejected(callback_query: types.CallbackQuery):
    await callback_query.answer(text="rejected",
                                show_alert=True)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(AdminStates.all()[0])


@dp.message_handler(state=AdminStates.GET_REASON)
async def get_reason(message: types.Message):
    db_sess = db_session.create_session()
    if ((message.from_user.id == 5023078965) or
            (message.from_user.id in db_sess.query(User).filter(
                User.privilege_level == 1))):
        await bot.send_message(message.from_user.id, MESSAGES["get_reason"],
                               reply_markup=empty_markup)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(AdminStates.all()[1])


@dp.message_handler(state=AdminStates.SEND_REJECTED)
async def send_rejected(message: types.Message):
    db_sess = db_session.create_session()
    state = dp.current_state(user=message.from_user.id)
    if ((message.from_user.id == 5023078965) or
            (message.from_user.id in db_sess.query(User).filter(
                User.privilege_level == 1))):
        d = await state.get_data()
        await bot.send_message(d["from_user_id"], MESSAGES["was_rejected"],
                               reply_markup=empty_markup)
    await state.finish()

