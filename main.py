import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import db_session
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

from conversations.take_away_admin.handlers import *

from conversations.admin.handlers import *

from conversations.user.handlers import *


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':  # press F
    db_session.global_init("db/SmartSender.db")
    executor.start_polling(dp, on_shutdown=shutdown)
