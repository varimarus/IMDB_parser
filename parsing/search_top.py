from dotenv import find_dotenv, load_dotenv
from bot_admin.other_data import headers_imdb, keys_for_top
from parsing.search_movie import Movie
import os
import json
import requests

load_dotenv(find_dotenv())


class Top:

    @classmethod
    def search_top(cls, limit: int, genre_n: str) -> list:
        """
        Функия поиска топ фильмов по жанру выбранным пользователем
        :param limit: Лимит поисковой выдачи
        :param genre_n: Вводимый жанр для выполнения GET запроса
        :return: результат GET запроса
        """
        response = requests.Session()
        querystring = {"genre": genre_n, "limit": limit}
        answer = response.get(os.getenv('url_top'), headers=headers_imdb, params=querystring)
        temp_list: list = list()
        for item in json.loads(answer.text):
            temp_list.append(item[7:-1])

        return temp_list

    @classmethod
    def filter_title(cls, title: list) -> dict:
        """
        Функция фильтрации фильмов в Топе по заданным ключам
        :param title: Список символьных названия фильмов
        :return: отфильтрованный список фильмов
        """
        out_data: dict = dict()
        for name in title:
            temp_data: dict = Movie.search_title(
                title=name,
                url=os.getenv('url_tittle'),
                mode='tconst'
            )
            temp_dict: dict = dict()
            for item, value in temp_data['title'].items():

                if item == 'id':
                    temp_dict['id'] = value[7:-1]
                elif item in keys_for_top:
                    temp_dict[item] = value
            out_data[temp_data['title']['title']] = temp_dict
        return out_data


if __name__ == '__main__':

    temp = Top.search_top(limit=5, genre_n='drama')
    print(Top.filter_title(temp))
