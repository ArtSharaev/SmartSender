import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config.config import TOKEN

logging.basicConfig(filename='telegram_bot.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s -'
                           '%(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await bot.send_message(msg.from_user.id,
                           "Привет от разработчиков!\n\nЗаполните анкету,"
                           " чтобы получить доступ к функционалу.",
                           reply_markup=start_anket_kb)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    start_anket_kb = ReplyKeyboardMarkup()
    start_anket_kb.add(KeyboardButton('СОЗДАТЬ АНКЕТУ'))
    executor.start_polling(dp)
