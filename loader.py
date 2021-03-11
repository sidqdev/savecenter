from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.mongo import MongoStorage


storage = MongoStorage(host='localhost', port=27017, db_name='aiogram_fsm')


API = '1365927493:AAGwlRZpEpWyDTFl4jF0l6fhoxrYMpMaxyU'
# API = '1519913388:AAFReunM6q-zyNjVll6YizuxTyrwvnPsl8s'
bot = Bot(token=API, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

