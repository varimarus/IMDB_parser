from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


class ReplyKeyboard:

    @classmethod
    def builder_button(cls, name_button: tuple) -> ReplyKeyboardMarkup:
        """
        Функция для создания экземпляра клавиатуры по заданным названиям
        :param name_button: Название кнопки
        :return: экземпляр клавиатуры
        """
        kb = ReplyKeyboardMarkup(row_width=3)
        for item in name_button:
            kb.insert(KeyboardButton(item))
        return kb

    @classmethod
    def remove_top_kb(cls, func):
        """
        Функция для удаления клавиатуры
        :return: Экземпляр клавиатуры переданный другой функцией
        """
        ReplyKeyboardRemove()
        return func


