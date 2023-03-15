from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from keyboard import in_Keyboard_more, ReplyKeyboard
from bot_admin import bot
from bot_admin.other_data import button_top_first, button_top_second, button_top_limit, dict_top
from parsing.search_top import Top
from functions.other_func import OtherFunc
from db_sql.db_function import Functions
from db_sql import db_create as db
from dotenv import find_dotenv, load_dotenv
from datetime import datetime


load_dotenv(find_dotenv())


class FsmTop(StatesGroup):
    start = State()
    check_genre = State()


async def start_top(message: types.Message) -> None:
    await message.answer(
        text='Добро пожаловать в раздел поиска Топ фильмов по жанру'
             '\n Выберите Жанр из списка',
        reply_markup=ReplyKeyboard.builder_button(button_top_first))
    await FsmTop.start.set()


async def next_genre(message: types.Message) -> None:
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Сменили жанры',
        reply_markup=ReplyKeyboard.remove_top_kb(ReplyKeyboard.builder_button(button_top_second)))


async def previous_genre(message: types.Message) -> None:
    await message.delete()
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Сменили жанры',
        reply_markup=ReplyKeyboard.remove_top_kb(ReplyKeyboard.builder_button(button_top_first)))


async def genre_check(message: types.Message, state: FSMContext) -> None:
    if message.text in dict_top.keys():
        await FsmTop.next()
        async with state.proxy() as data:
            data['genre'] = dict_top[message.text]
        await message.answer(
            text='Выберите лимит выдачи результата',
            reply_markup=ReplyKeyboard.remove_top_kb(ReplyKeyboard.builder_button(button_top_limit))
        )


async def top_genre(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        text='Помните! Чем больше выборка, тем дольше ждать %)',
        reply_markup=ReplyKeyboardRemove()
    )
    try:
        if 100 >= int(message.text) >= 10:
            async with state.proxy() as data:
                title_list: list = Top.search_top(limit=int(message.text), genre_n=data['genre'])
            temp_filter: dict = Top.filter_title(title=title_list)
            for item, values in temp_filter.items():
                try:
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text='Оригинальное название - {name}\nTime - {time}\nГод выпуска - {years}'.format(
                            name=item,
                            years=values['year'],
                            time=OtherFunc.convert_time(values['runningTimeInMinutes'])),
                        reply_markup=in_Keyboard_more
                    )
                except KeyError:
                    pass
            Functions.insert_user(
                user_id=message.from_user.id,
                user_name=message.from_user.full_name,
                command='movie_top',
                desired=message.text,
                date=datetime.today().isoformat(sep=' ', timespec='seconds')
            )
            Functions.insert_in_db(
                user_id=message.from_user.id,
                desired='Топ - {genre}'.format(genre=data['genre']),
                result=temp_filter,
                method=db.Movie
            )
        else:
            await message.answer(
                text='Выберите правильное значение в диапазоне от 10 до 100'
            )
    except ValueError:
        await message.answer(
            text='Введите или выберите числовое значение'
        )
    await message.answer(text='Поиск завершен :)', reply_markup=ReplyKeyboardRemove())
    await state.finish()


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_top, commands='search_top', state=None)
    dp.register_message_handler(next_genre, Text(equals='Другие жанры ->', ignore_case=True), state=FsmTop.start)
    dp.register_message_handler(previous_genre, Text(equals='<- Предыдущие', ignore_case=True), state=FsmTop.start)
    dp.register_message_handler(genre_check, state=FsmTop.start)
    dp.register_message_handler(top_genre, state=FsmTop.check_genre)
