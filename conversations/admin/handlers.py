"""Машина состояний для работы админа"""

from aiogram import types
import datetime as dt

from conversations.admin.keyboards import form_markup, start_markup,\
    empty_markup
from conversations.admin.utils import AdminStates
from conversations.admin.messages import MESSAGES
from conversations.admin.keyboards import admin_markup
from conversations.user.keyboards import user_markup

from data import db_session
from data.form_table import Form
from data.users_table import User

from main import dp, bot


def check_admin(user_id):
    db_sess = db_session.create_session()
    for user in db_sess.query(User).filter(User.privilege_level == 1).all():
        if user_id == user.id:
            return True
    return False


@dp.message_handler(commands=['getform'])
async def getform_command(message: types.Message):
    db_sess = db_session.create_session()
    print(db_sess.query(User).filter(User.privilege_level == 1).all())
    if (message.from_user.id == 5023078965 or
            check_admin(message.from_user.id)):
        form = db_sess.query(Form).filter(Form.status == 0).first()
        if form:
            msg = f"""
              Анкета номер {str(form.id)}:
            Создана {str(form.created_date)}
            {form.name} {form.surname}
            Возраст: {str(form.age)}
            Пол: {form.gender}
            {form.position}
            """
            state = dp.current_state(user=message.from_user.id)
            await state.update_data(from_user_id=form.from_tg_user_id)
            await state.update_data(form_id=form.id)
            await bot.send_message(message.from_user.id, msg,
                                   reply_markup=form_markup)
        else:
            await bot.send_message(message.from_user.id, MESSAGES["no_forms"],
                                   reply_markup=empty_markup)


@dp.callback_query_handler(text='accept_form')
async def form_accepted(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    db_sess = db_session.create_session()
    state = dp.current_state(user=callback_query.from_user.id)
    d = await state.get_data()
    form = db_sess.query(Form).filter(Form.id == d["form_id"]).first()
    form.status = 2
    form.moderator_id = callback_query.from_user.id
    form.changed_date = dt.datetime.now()
    user = User()
    user.id = d["from_user_id"]
    user.privilege_level = 0
    user.name = form.name
    user.surname = form.surname
    user.gender = form.gender
    user.age = form.age
    user.position = form.position
    user.form_id = form.id
    db_sess.add(user)
    db_sess.commit()
    await bot.send_message(callback_query.from_user.id,
                           MESSAGES["was_accepted"],
                           reply_markup=admin_markup)
    await bot.send_message(d["from_user_id"], MESSAGES["accepted_message"],
                           reply_markup=user_markup)
    await state.finish()


@dp.callback_query_handler(text='reject_form')
async def form_rejected(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, MESSAGES["get_reason"],
                           reply_markup=empty_markup)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(AdminStates.all()[0])


@dp.message_handler(state=AdminStates.SEND_REJECTED)
async def send_rejected(message: types.Message):
    db_sess = db_session.create_session()
    state = dp.current_state(user=message.from_user.id)
    d = await state.get_data()
    print(d["from_user_id"])
    from_user_id = d["from_user_id"]
    form_id = d["form_id"]
    form = db_sess.query(Form).filter(Form.id == form_id).first()
    form.status = 1
    form.moderator_id = message.from_user.id
    form.changed_date = dt.datetime.now()
    db_sess.commit()
    await bot.send_message(message.from_user.id,
                           MESSAGES["was_rejected"],
                           reply_markup=admin_markup)
    await bot.send_message(from_user_id,
                           MESSAGES["rejected_message"] +
                           message.text + MESSAGES["enter_start"],
                           reply_markup=start_markup)
    await state.finish()

