"""Машина состояний для того, чтобы забирать роль админов у пользователей"""

from aiogram import types

from conversations.take_away_admin.utils import TakeAwayAdminStates
from conversations.take_away_admin.messages import MESSAGES
from conversations.user.keyboards import user_markup

from data import db_session
from data.users_table import User

from main import dp, bot


@dp.message_handler(commands=['takeawayadmin'])
async def takeawayadmin_command(message: types.Message):
    if message.from_user.id == 5023078965:
        await bot.send_message(message.from_user.id, MESSAGES['ask_user'])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TakeAwayAdminStates.all()[0])


@dp.message_handler(state=TakeAwayAdminStates.ASK_REASON)
async def ask_reason(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(user_id=int(message.text))
    await bot.send_message(message.from_user.id, MESSAGES['ask_reason'])
    await state.set_state(TakeAwayAdminStates.all()[1])


@dp.message_handler(state=TakeAwayAdminStates.NOTIFY_USER)
async def notify_user(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    d = await state.get_data()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id
                                      == d["user_id"]).first()
    print(user)
    user.privilege_level = 0
    db_sess.commit()
    await bot.send_message(d["user_id"],
                           f"{MESSAGES['take_away_notify']} {message.text}",
                           reply_markup=user_markup)
    await bot.send_message(5023078965,
                           f"{MESSAGES['ok_message']} {d['user_id']}")
    await state.finish()
