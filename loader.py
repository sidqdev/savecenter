from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.mongo import MongoStorage
import os

storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')

#

API = str(os.getenv('scapi'))
bot = Bot(token=API, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

