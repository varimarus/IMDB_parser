from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cd = CallbackData('in_Keyboard_1', 'action')

button_1 = InlineKeyboardButton(text='Посмотреть подробнее', callback_data=cd.new('more'))
button_2 = InlineKeyboardButton(text='Добавить в избранное', callback_data=cd.new('favorite'))
in_Keyboard_more = InlineKeyboardMarkup().add(button_1)
in_Keyboard_favorite = InlineKeyboardMarkup().add(button_2)



