import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s]'
                           u' %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    filename='tgbot.log',
                    filemode='w')
dp.middleware.setup(LoggingMiddleware())

from conversations.give_admin.handlers import *

from conversations.profile.handlers import *

from conversations.mode_selection.handlers import *

from conversations.take_away_admin.handlers import *


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


@dp.message_handler()
async def echo(msg: types.Message):
    print(f"Получено сообщение '{msg.text}' от пользователя {msg.from_user.id}")


if __name__ == '__main__':  # press F
    executor.start_polling(dp, on_shutdown=shutdown)
