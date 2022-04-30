"""Машина состояний для составления анкеты"""

from aiogram import types

from conversations.mode_selection.utils import ModeSelectionStates
from conversations.mode_selection.messages import MESSAGES
from conversations.mode_selection.keyboards import ask_admin_markup, empty_markup

from main import dp, bot


@dp.message_handler(commands=['giveadmin'])
async def give_admin(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id == 5023078965:
        await bot.send_message(message.from_user.id, MESSAGES['askuser'],
                               reply_markup=empty_markup)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(ModeSelectionStates.all()[1])


@dp.message_handler(state=ModeSelectionStates.GIVE_ADMIN)
async def ask_admin(message: types.Message):
    if message.from_user.id == 5023078965:
        await bot.send_message(int(message.text), MESSAGES['askadmin'],
                               reply_markup=ask_admin_markup)
    # state = dp.current_state(user=message.from_user.id)
    # await state.set_state(ModeSelectionStates.all()[0])


@dp.callback_query_handler(text='yes_pressed')
async def pressed_yes(callback_query: types.CallbackQuery):
    print(12122)
    # await bot.answer_callback_query(callback_query.id)
    # await bot.send_message(callback_query.from_user.id,
    #                        'Поздравляем, теперь вы админ!')
    await callback_query.answer()
    await callback_query.message.answer(text="Спасибо, что воспользовались ботом!")
#
#
# @dp.callback_query_handler(func=lambda c: c.data == 'no_pressed')
# async def pressed_no(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Хорошо')


@dp.message_handler()
async def echo_message(msg: types.Message):
    print(msg.from_user.id)
    await bot.send_message(msg.from_user.id, msg.text)

