from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboard import in_Keyboard_more, in_Keyboard_favorite, ReplyKeyboard, cd
from datetime import datetime
from functions.other_func import OtherFunc
from db_sql.db_function import Functions
from db_sql import db_create as db
from bot_admin import bot
from bot_admin.other_data import button_film, keys
from parsing.search_movie import Movie
from parsing.translate import translate
from typing import Any
from dotenv import find_dotenv, load_dotenv
import os
import json


load_dotenv(find_dotenv())


class FSMFilm(StatesGroup):
    start = State()
    search = State()


async def start_movie(message: types.Message) -> None:
    await message.delete()
    await message.answer(
        text='Добро пожаловать в раздел поиска Кинолент\n Введите название для поиска:',
        reply_markup=ReplyKeyboardRemove()
                         )
    await FSMFilm.start.set()


async def search_movie(message: types.Message, state: FSMContext) -> None:
    Functions.insert_user(
        user_id=message.from_user.id,
        user_name=message.from_user.full_name,
        command='search_movie',
        desired=message.text,
        date=datetime.today().isoformat(sep=' ', timespec='seconds')
    )
    result:  bool | list | dict = Movie.search_title(message.text, os.getenv('url_movie'))
    if result:
        await message.reply('Вот что удалось найти:\n')
        for key, value in Movie.filter_title(result).items():
            try:
                await message.answer(
                    'Оригинальное название - {name} \nГод выпуска - {year} '.format(
                        name=key,
                        year=value['year']
                    ),
                    reply_markup=in_Keyboard_more
                )
            except KeyError:
                pass
        Functions.insert_in_db(
            user_id=message.from_user.id,
            desired=message.text,
            result=Movie.filter_title(result),
            method=db.Movie
        )
    else:
        await message.reply('Результат не найден\nПовторите поиск')
        await state.reset_state()
    await state.finish()
    await message.answer('Поиск завершен', reply_markup=ReplyKeyboard.builder_button(button_film))


async def start_action(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    await message.answer(
        text='Добро пожаловать в раздел поиска Кинолент\n Введите название для поиска:',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(state=FSMFilm.start)


async def more_detail(callback: types.CallbackQuery, callback_data: dict) -> None:
    id_user: int = callback.from_user.id
    if callback_data['action'] == 'more':
        await bot.send_message(chat_id=id_user, text='Уточняем детали %) Подождите немного')
        message: bool = False
        name_title: str = callback.message.text[24:-20:]
        id_movie: Any = Functions.search_id_title(user_id=id_user, method=db.Movie, title=name_title)
        try:
            full_data: dict = Movie.search_title(title=id_movie, url=os.getenv('url_tittle'), mode='tconst')
        except json.decoder.JSONDecodeError:
            name_title: str = callback.message.text.split(' - ')[1][:-5]
            id_movie: Any = Functions.search_id_title(
                user_id=id_user,
                method=db.Movie,
                title=name_title
            )
            try:
                full_data: dict = Movie.search_title(title=id_movie, url=os.getenv('url_tittle'), mode='tconst')
            except json.decoder.JSONDecodeError:
                name_title: str = callback.message.text.split(' - ')[1]
                id_movie: Any = Functions.search_id_title(
                    user_id=id_user,
                    method=db.Movie,
                    title=name_title)
                full_data: dict = Movie.search_title(title=id_movie, url=os.getenv('url_tittle'), mode='tconst')
        details_data: dict = dict()
        ru_name: str = translate(in_lang='en', out_lang='ru', new_text=name_title)
        for item in keys:
            Movie.filter_to_detail(struct=full_data, key=item, out_data=details_data)
        for item in keys:
            try:
                details_data[item]
            except KeyError:
                message = True
        if message:
            await bot.send_message(chat_id=id_user, text=f'Данные о картине {name_title} не найдены')
        else:
            await bot.send_photo(
                chat_id=id_user, photo=details_data['url'],
                caption='Оригинальное название - {origin}\n'
                        'Название - {name}'
                        '\nГод выпуска - {year}'
                        '\nПродолжительность - {time}'
                        '\nТип видео - {type}'
                        '\nРейтинг IMDb - {rat}'
                        '\nЖанры - {genre}'
                        '\nКраткий обзор - {text}'.format(
                    name=ru_name,
                    origin=name_title,
                    year=details_data['year'],
                    time=OtherFunc.convert_time(details_data['runningTimeInMinutes']),
                    type=translate(in_lang='en', out_lang='ru', new_text=details_data['titleType']),
                    rat=details_data['rating'],
                    genre=details_data['genres'],
                    text=translate(in_lang='en', out_lang='ru', new_text=details_data['text'])
                ),
                reply_markup=ReplyKeyboard.remove_top_kb(in_Keyboard_favorite)
            )

    elif callback_data['action'] == 'favorite':
        insert_text = callback.message['caption'].split(' - ')[1][:-9]
        if Functions.update_favorites(
            user_id=id_user,
            desired='Добавление в Избранное',
            result=insert_text
        ):
            await bot.send_message(
                chat_id=id_user,
                text=f'{insert_text} - Успешно добавили в избранное'
            )
        else:
            await bot.send_message(
                chat_id=id_user,
                text=f'{insert_text} - Уже добавлен в ваше избранное'
            )


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_movie, commands='search_movie', state=None)
    dp.register_message_handler(search_movie, state=FSMFilm.start)
    dp.register_message_handler(start_action, Text(equals='Повторить поиск Фильма', ignore_case=True), state='*')
    dp.register_callback_query_handler(more_detail, cd.filter())

