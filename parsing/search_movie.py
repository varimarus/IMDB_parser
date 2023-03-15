from typing import Any
from dotenv import find_dotenv, load_dotenv
from bot_admin.other_data import headers_imdb, keys_for_top
import os
import json
import requests

load_dotenv(find_dotenv())


class Movie:
    @classmethod
    def search_title(cls, title: str, url: str, mode: str = 'q') -> bool | list | dict:
        """
        Функция поиска фильмов по запросу пользователя
        :param title: Название фильма для поиска
        :param url: URL для выполнения GET запроса
        :param mode: Режим выполнения GET запроса
        :return: Результат запроса ввиде словаря
        """
        response = requests.Session()
        querystring = {mode: title}
        answer = response.get(url=url, headers=headers_imdb, params=querystring)
        try:
            if mode == 'q':
                return json.loads(answer.text)['results']
            else:
                return json.loads(answer.text)
        except KeyError:
            print('Поиск результата не дал')
            return False

    @classmethod
    def filter_title(cls, data: list) -> dict:
        """
        Функция фильтрации фильмов по заданным ключам
        :param data: Словарь для сортировки
        :return: Отсортированный словарь по заданным ключам
        """
        new_data: dict[str, Any] = dict()
        out_dict: dict[str, Any] = dict()
        name = None
        for new in data:
            for key, item in new.items():
                if key == 'id':
                    new_data[key] = item[7:-1:]
                elif key == 'year':
                    new_data[key] = item
                elif key == 'title':
                    name = item
            out_dict[name] = new_data
            new_data: dict[str, Any] = dict()
        return out_dict

    @classmethod
    def filter_to_detail(cls, struct: dict, key: str, out_data: dict) -> dict:
        """
        Рекурсивная Функция фильтрации данных по списку ключей в выбранной сруктуре
        :param struct: Передаваяемая структура для выполнения фильтрации
        :param key: Ключ для поиска в структуре
        :param out_data: Словарь для добавления результата поиска
        :return: результат фильтрации данных
        """
        if key in struct:
            if isinstance(struct[key], list):
                out_data[key] = ', '.join(struct[key])
                return out_data
            else:
                out_data[key] = struct[key]
                return out_data
        for sub_struct in struct.values():
            if isinstance(sub_struct, dict):
                result = Movie.filter_to_detail(sub_struct, key, out_data)
                if result:
                    return out_data


if __name__ == '__main__':
    titles = Movie.search_title('tt5635026', os.getenv('url_tittle'), mode='tconst')
    details_data: dict = dict()
    for item in keys_for_top:
        Movie.filter_to_detail(titles, item, details_data)
    print(details_data)
    print(titles)

