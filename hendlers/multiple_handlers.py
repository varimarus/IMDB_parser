from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboard import in_Keyboard_more
from db_sql.db_function import Functions
from db_sql import db_create as db
from bot_admin import bot


async def start_menu(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer(
        text='Выберите из команд, что вас интересует:\n'
             '/search_movie - Поиск фильмов по названию\n'
             '/search_actor - Поиск информации по актеру\n'
             '/search_top - Поиск фильмов в топ рейтинге\n'
             '/favorites - Избранные фильмы добавленные вами\n'
             '/translate - Переводчик\n'
             '/help - Помошь (описание работы бота)\n'
             '/history - Посмотреть историю взаимодействия с Ботом\n'
             '/stop - Остановить бота',
        reply_markup=ReplyKeyboardRemove()
    )


async def stop(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    await state.finish()
    await message.answer(
            text='Бот остановлен',
            reply_markup=ReplyKeyboardRemove()
        )


async def get_favorite(message: types.Message) -> None:
    user_id = message.from_user.id
    await message.delete()
    try:
        result: list = eval(db.Favorites.get(db.Favorites.user_id == user_id).result)
        count: int = 1
        for item in result:
            await bot.send_message(
                chat_id=user_id,
                text=f'У вас в избранном: {count} - {item}',
                reply_markup=in_Keyboard_more
            )
            count += 1
    except BaseException:
        await bot.send_message(
            chat_id=user_id,
            text='У вас не добавлено ни одного фильма'
        )


async def history_search(message: types.Message) -> None:
    id_user = message.from_user.id
    for item in Functions.get_history(user_id=id_user):
        await bot.send_message(
            chat_id=id_user,
            text=f"Режим - {item.user_command}"
                 f"\nЗапрос - {item.user_search}"
                 f"\nДата и время запроса - {item.datetime_search}"
        )


async def user_help(message: types.Message) -> None:
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Здравствуйте! В этом разделе мы познакомим вас с основными принципами работы данного бота.'
             'Вам доступны следующие команды:\n'
             '/search_movie - Модуль для поиска фильмов по названию.'
             ' Результатом будет выборка фильмов по введенному названию с учетом всех совпадений на сервисе.'
             'У каждой кинокартины есть возможность посмотреть подробную информацию. Используемый язык - Русский\n'
             '/search_actor - Модуль для поиска информации о актерах мирового кино.'
             ' Результатом будет краткая биография о актере'
             ' и возможность посмотреть полную фильмографию актера с возможностью посмотреть подробную информацию'
             'Используемый язык - Русский.'
             ' Важно: поиск актера основан на трансляции русского имени в английский вариант, особенность сервиса,'
             'это может привести к неправильному поиску и отрицательном результате поиска.\n'
             '/search_top - Модуль для формирования списка топ фильмов в рейтинге пользователей.'
             ' Поиск осуществляется по жанру.\n'
             '/favorites - Модуль в котором вы сможете посмотреть избранные фильмы, которые были добавлены вами\n'
             '/translate - Модуль для перевода текста. Классический переводчик, но с ограниченым количеством языков.\n'
             '/history - Модуль в котором можно посмотреть историю взаимодействия с основными модулями бота.\n'
             '/stop - Команда для остановки работы бота на любом этапе взаимодействия'
    )


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_menu, Text(equals='Перейти в меню', ignore_case=True), state='*')
    dp.register_message_handler(start_menu, commands='start', state='*')
    dp.register_message_handler(stop, commands='stop', state='*')
    dp.register_message_handler(get_favorite, commands='favorites', state=None)
    dp.register_message_handler(history_search, commands='history', state=None)
    dp.register_message_handler(user_help, commands='help', state=None)
