from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
import os


load_dotenv(find_dotenv())
new_storage = MemoryStorage()


bot = Bot(os.getenv('token_API'))
dp = Dispatcher(bot, storage=new_storage)
