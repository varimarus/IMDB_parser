from aiogram import types
from db_sql.db_create import create_database
from dotenv import find_dotenv, load_dotenv
import os


load_dotenv(find_dotenv())


async def set_default_commands(dp):
    """
    Функция установки команд для бота
    :param dp: Диспетчер
    :return: None
    """
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("search_movie", "Приступить к поиску фильма по названию"),
        types.BotCommand("search_actor", "Приступить к поиску актера по имени"),
        types.BotCommand("search_top", "Приступить к поиску топ фильма по параметрам"),
        types.BotCommand("favorites", "Посмотреть избранное"),
        types.BotCommand("translate", "Переводчик (опционально)"),
        types.BotCommand("stop", "Остановить Бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("history", "История взаимодействия с ботом"),
    ])


async def set_database():
    """
    Функция проверки Базы данных, в случае отсутствия создание
    :return: None
    """
    if os.path.exists(os.getenv('path_db')):
        print('База данных подключена')
    else:
        create_database()
        print('База данных создана и подключена')
