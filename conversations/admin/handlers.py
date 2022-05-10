"""Машина состояний для работы админа"""

from aiogram import types

from conversations.admin.keyboards import form_markup, empty_markup

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
        await bot.send_message(message.from_user.id, msg,
                               reply_markup=form_markup)


@dp.callback_query_handler(text='accept_form')
async def pressed_yes(callback_query: types.CallbackQuery):
    await callback_query.answer(text="ok",
                                show_alert=True)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)


@dp.callback_query_handler(text='reject_form')
async def pressed_no(callback_query: types.CallbackQuery):
    await callback_query.answer(text="rejected",
                                show_alert=True)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)

