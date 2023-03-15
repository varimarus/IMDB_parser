from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboard.replykeyboard import ReplyKeyboard
from parsing.translate import translate
from bot_admin.other_data import dict_translate, button_translate
from db_sql.db_function import Functions
from db_sql import db_create as db
from datetime import datetime


class FSMtranslate(StatesGroup):
    start = State()
    source = State()
    target = State()


async def start_translate(message: types.Message) -> None:
    await message.delete()
    await message.answer(
        text='Добро пожаловать в раздел - Переводчик\n'
             'Для выхода из Переводчика введите:\n'
             '/stop\n '
             'Выберите язык оригинала\n',
        reply_markup=ReplyKeyboard.builder_button(button_translate)
    )
    await FSMtranslate.start.set()


async def source_lang(message: types.Message, state: FSMContext) -> None:
    if message.text.title() in dict_translate.keys():
        name: str = message.from_user.full_name
        async with state.proxy() as data:
            data['source'] = dict_translate[message.text.title()]
        await message.answer(
            text=f"{name}, вы выбрали язык для перевода- {message.text}\n"
                 f"Теперь выберите язык на который хотите перевести"
        )
        await FSMtranslate.next()
    else:
        await message.answer(
            text=' Ошибка ввода. Выберите правильный язык\n'
                 'Для выхода из Переводчика введите:\n'
                 '/stop'
        )


async def target_lang(message: types.Message, state: FSMContext) -> None:
    if message.text.title() in dict_translate.keys():
        name: str = message.from_user.full_name
        async with state.proxy() as data:
            data['target'] = dict_translate[message.text.title()]
        await message.answer(
            text=f"{name}, вы выбрали язык на который необходим перевод- {message.text}\n"
                 f"Теперь введите текст для перевода",
            reply_markup=ReplyKeyboardRemove()
        )
        await FSMtranslate.next()
    else:
        await message.answer(
            text=' Ошибка ввода. Выберите правильный язык\n'
                 'Для выхода из Переводчика введите:\n'
                 '/stop'
        )


async def text(message: types.Message, state: FSMContext) -> None:
    Functions.insert_user(
        user_id=message.from_user.id,
        user_name=message.from_user.full_name,
        command='translate',
        desired=message.text,
        date=datetime.today().isoformat(sep=' ', timespec='seconds')
    )
    await message.answer(
        text='Пробуем перевести ваш текст'
    )
    async with state.proxy() as data:
        data['text'] = message.text
        answer: str = translate(
            in_lang=data['source'],
            out_lang=data['target'],
            new_text=data['text']
        )
    await message.answer(
        text=f'Ваш перевод:\n'
             f'{answer}'
    )
    Functions.insert_in_db(
        user_id=message.from_user.id,
        desired=data['text'],
        result=answer,
        method=db.Translate)
    await state.finish()


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_translate, commands=["translate"], state=None)
    dp.register_message_handler(source_lang, state=FSMtranslate.start)
    dp.register_message_handler(target_lang, state=FSMtranslate.source)
    dp.register_message_handler(text, state=FSMtranslate.target)


