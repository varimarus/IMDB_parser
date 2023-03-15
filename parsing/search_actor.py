from dotenv import find_dotenv, load_dotenv
from parsing.translate import translate
from bot_admin import headers_imdb, keys_actor
import os
import json
import requests

load_dotenv(find_dotenv())


class Actor:

    @classmethod
    def get_name_id(cls, name: str) -> str:
        """
        Функция для получения ID имени актера
        :param name: Имя актера
        :return: ID имени актера
        """
        name: str = translate(in_lang='ru', out_lang='en', new_text=name)
        querystring = {"q": name}
        response = requests.Session()
        answer = response.get(
            os.getenv('url_get_name'),
            headers=headers_imdb,
            params=querystring
        )
        for item in json.loads(answer.text)['d']:
            if item['s'].startswith('Actor')\
                    or item['s'].startswith('Actress')\
                    or item['s'].startswith('Produser')\
                    or item['s'].startswith('Writer'):
                return item['id']

    @classmethod
    def get_date(cls, name: str, url: str) -> dict:
        """
        Функция получения GET-данных о искомом Актере
        :param name: Имя Актера
        :param url: URL для выполнения запроса
        :return: Результат запроса ввиде словаря
        """
        querystring = {'nconst': name}
        response = requests.Session()
        answer = response.get(
            url,
            headers=headers_imdb,
            params=querystring
        )
        return json.loads(answer.text)

    @classmethod
    def sort_bio(cls, data: dict) -> dict:
        """
        Функция сортировки данных Актера по заданным ключам
        :param data: Словарь данных
        :return: Отсортированный словарь по ключам
        """
        temp_dict: dict = dict()
        for item, values in data.items():
            if item == 'id':
                temp_dict[item] = values[6:-1:]
            elif item == 'image':
                temp_dict['image'] = values['url']
            elif item in keys_actor:
                temp_dict[item] = values
            elif item == 'miniBios':
                temp_dict[item] = '\n'.join(values[0]['text'].split('\n\n')[:2])
        return temp_dict

    @classmethod
    def sort_filmography(cls, data) -> dict:
        """
        Функция сортировки фильмографии Актера
        :param data: Словарь для сортировки
        :return: Отсортированный словарь
        """
        out_dict: dict = dict()
        temp_dict: dict = dict()
        for item in data['filmography']:
            if item['titleType'] == 'movie':
                for key, values in item.items():
                    if key == 'characters':
                        temp_dict[key] = values[0]
                    elif key == 'id':
                        temp_dict[key] = values[7:-1:]
                    elif key == 'year':
                        temp_dict[key] = values
                out_dict[item['title']] = temp_dict
                temp_dict = dict()
        return out_dict


if __name__ == '__main__':
    all_data = Actor.get_name_id(name='квентин тарантино')
    all_bio = Actor.get_date(name=all_data, url=os.getenv('url_get_bio'))
    print(all_data)
    print(all_bio)


