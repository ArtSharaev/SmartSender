"""Машина состояний для выбора режима работы"""

from aiogram import types

from conversations.mode_selection.keyboards import empty_markup,\
    select_mode_markup
from conversations.mode_selection.messages import MESSAGES

from main import dp, bot


@dp.message_handler(commands=['selectmode'])
async def selectmode_command(message: types.Message):
    await message.reply(MESSAGES['select_mode'],
                        reply_markup=select_mode_markup, reply=False)


@dp.callback_query_handler(text='user')
async def pressed_user(callback_query: types.CallbackQuery):
    await callback_query.answer(text=MESSAGES["user_selected"])
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)


@dp.callback_query_handler(text='admin')
async def pressed_admin(callback_query: types.CallbackQuery):
    await callback_query.answer(text=MESSAGES["admin_selected"])
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
