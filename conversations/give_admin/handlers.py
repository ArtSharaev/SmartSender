"""Машина состояний для добавления админов"""

from aiogram import types

from conversations.give_admin.utils import GiveAdminStates
from conversations.give_admin.messages import MESSAGES
from conversations.give_admin.keyboards import ask_admin_markup, empty_markup

from main import dp, bot


@dp.message_handler(commands=['giveadmin'])
async def giveadmin_command(message: types.Message):
    if message.from_user.id == 5023078965:
        await bot.send_message(message.from_user.id, MESSAGES['ask_user'],
                               reply_markup=empty_markup)
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
    await callback_query.answer(text=MESSAGES["admin_greeting"],
                                show_alert=True)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)


@dp.callback_query_handler(text='no_pressed')
async def pressed_no(callback_query: types.CallbackQuery):
    await callback_query.answer(text=MESSAGES["admin_negate"],
                                show_alert=True)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)

