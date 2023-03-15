from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from keyboard import in_Keyboard_more, ReplyKeyboard
from db_sql.db_function import Functions
from db_sql import db_create as db
from bot_admin import bot
from bot_admin.other_data import button_actor
from parsing.translate import translate
from parsing.search_actor import Actor

import os
import json


load_dotenv(find_dotenv())


class FSMActor(StatesGroup):
    start = State()
    search = State()


async def start_actor(message: types.Message) -> None:

    await message.delete()
    await message.answer(
        text='Добро пожаловать в раздел поиска Информации о актерах\n Введите имя актера для поиска:',
        reply_markup=ReplyKeyboardRemove()
    )
    await FSMActor.start.set()


async def search_actor(message: types.Message, state: FSMContext) -> None:
    Functions.insert_user(
        user_id=message.from_user.id,
        user_name=message.from_user.full_name,
        command='search_actor',
        desired=message.text,
        date=datetime.today().isoformat(sep=' ', timespec='seconds')
    )
    await message.answer(text=f'Ищем информацию о {message.text}')
    user_id: int = message.from_user.id
    name_id: str = Actor.get_name_id(name=message.text)
    try:
        sort_bio: dict = Actor.sort_bio(data=Actor.get_date(name=name_id, url=os.getenv('url_get_bio')))
        await bot.send_photo(
            chat_id=user_id,
            photo=sort_bio['image'],
            caption='Полное имя: {name}'
                    '\n Дата рождения: {birth}'
                    '\n Рост: {height} см.'
                    '\n Место рождения: {place}'.format(
                name=sort_bio['realName'],
                birth=sort_bio['birthDate'],
                height=sort_bio['heightCentimeters'],
                place=sort_bio['birthPlace']
                )
        )
        await bot.send_message(
            chat_id=user_id,
            text='Краткая биография: {bio}'.format(
                bio=translate(in_lang='en', out_lang='ru', new_text=sort_bio['miniBios'])),
            reply_markup=ReplyKeyboard.builder_button(button_actor)
        )
        Functions.insert_in_db(
            user_id=message.from_user.id,
            desired=message.text,
            result=sort_bio,
            method=db.Actor
        )
        async with state.proxy() as data:
            data['id'] = sort_bio['id']
            data['name'] = sort_bio['realName']
        await FSMActor.next()
    except json.decoder.JSONDecodeError:
        await message.reply(text='Инофрмация не найдена, повторите ввод')
    except KeyError:
        await message.reply(text='Попробуйте повторить поиск')


async def all_filmography(message: types.Message, state: FSMContext) -> None:
    await message.delete()
    async with state.proxy() as data:
        id_actor: str = data['id']
    all_data: dict = Actor.get_date(name=id_actor, url=os.getenv('url_filmography'))
    all_film: dict = Actor.sort_filmography(data=all_data)
    Functions.insert_in_db(
        user_id=message.from_user.id,
        desired='Фильмография {data}'.format(data=data['name']),
        result=all_film,
        method=db.Movie
    )
    for item, values in all_film.items():
        try:
            await message.answer(
                'Оригинальное название - {name}\nРоль - {character} \nГод выпуска - {year} '.format(
                    name=item,
                    character=values['characters'],
                    year=values['year']
                ),
                reply_markup=in_Keyboard_more
            )
            await state.finish()
        except KeyError:
            pass
    await message.answer(text='Поиск завершен')


async def pass_massage(massage: types.Message):
    await massage.reply(text='Что нужно сделать?'
                             '\n/search_movie - поиск фильмов по названию\n'
                             '/search_actor - поиск информации по актеру\n'
                             '/search_top - поиск фильмов в топ рейтинге\n'
                             '/translate - переводчик\n'
                             '/stop - остановить бота')


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_actor, commands='search_actor', state=None)
    dp.register_message_handler(search_actor, state=FSMActor.start)
    dp.register_message_handler(start_actor, Text(equals='Повторить поиск Актера', ignore_case=True), state='*')
    dp.register_message_handler(all_filmography,
                                Text(equals='Посмотреть фильмографию', ignore_case=True),
                                state=FSMActor.search)
    dp.register_message_handler(pass_massage, state='*')

