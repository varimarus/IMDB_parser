from bot_admin import dp
from aiogram import executor
from bot_admin.config import set_default_commands, set_database
from hendlers import *


async def start_up(_):
    print("Бот Загрузился")
    await set_default_commands(dp)
    await set_database()

multiple_handlers.register_handlers(dp)
movie.register_handlers(dp)
translate.register_handlers(dp)
movie_top.register_handlers(dp)
actor.register_handlers(dp)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=start_up)
