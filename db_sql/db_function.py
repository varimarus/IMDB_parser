from db_sql import db_create as db
from typing import Any


class Functions:

    @classmethod
    def insert_user(cls, user_id: int, user_name: str, command: str, desired: str, date: Any) -> None:
        """
        Функция для добавления данных о пользователе в существующую базу данных
        :param user_id: ID телеграмм клиента
        :param user_name: Имя пользователя
        :param command: Выбранная команда бота
        :param desired: Результат выполнения команды
        :param date: Время запроса
        """
        db.User(
            telegram_id=user_id,
            user_name=user_name,
            user_command=command,
            user_search=desired,
            datetime_search=date
        ).save()

    @classmethod
    def insert_in_db(cls, user_id: int, desired: str, result: dict | str, method: Any) -> None:
        """
        Функция для добавления данных о пользователе в существующую базу данных
        :param user_id: ID телеграмм клиента
        :param desired: Запрос
        :param result: Результат запроса
        :param method: Таблица для записи данных
        :return:
        """
        method(
            user_id=user_id,
            request=desired,
            result=result
        ).save()

    @classmethod
    def insert_in_favorites(cls, user_id: int, desired: str, result: list | str) -> None:
        """
        Функция добавления избранного в существующую базу данных
        :param user_id: ID телеграмм клиента
        :param desired: Запрос
        :param result: Результат запроса
        :return:
        """
        db.Favorites(
            user_id=user_id,
            request=desired,
            result=result
        ).save()

    @classmethod
    def search_id_title(cls, user_id: int, method: Any, title: str) -> str:
        """
        Функция поиска ID Фильма в результатах поиска по сайту
        :param user_id: ID пользователя
        :param method: Таблица для поиска данных
        :param title: симвользное название фильма
        :return:
        """
        for item in method.select().where(method.user_id == user_id):
            try:
                return eval(item.result)[title]['id']
            except KeyError:
                pass

    @classmethod
    def update_favorites(cls, user_id: int, desired: str, result: str) -> bool:
        """
        Функция обновления избранного по ID пользователя
        :param user_id: ID телеграмм клиента
        :param desired: Запрос
        :param result: Результат запроса
        :return:
        """
        try:
            db_result: list = eval(db.Favorites.get(db.Favorites.user_id == user_id).result)
            if db_result.count(result) < 1:
                db_result.append(result)
                db.Favorites.update(result=db_result).where(db.Favorites.user_id == user_id).execute()
                return True
            else:
                return False
        except BaseException:
            new_record: list = list()
            print('not found, create new string')
            new_record.append(result)
            cls.insert_in_favorites(user_id=user_id, desired=desired, result=new_record)
            return True

    @classmethod
    def get_history(cls, user_id):
        """
        Функция для получения истории взаимодействия с ботом пользователя
        :param user_id: ID телеграмм клиент
        :return: итерируемый объект экземпляра базы данных для обращения по атрибуту базы данных
        """
        return db.User.select().where(db.User.telegram_id == user_id)


if __name__ == "__main__":
    zxc = db.Favorites.select().where(db.Favorites.user_id == 1011185293)

    db.Favorites.update(result=' 123').where(db.Favorites.user_id == 101118529).execute()
    try:
        asd = db.Favorites.get(db.Favorites.user_id == 1011185293).result
        print(asd)
    except BaseException:
        print('not found')

    vbn = Functions.get_history(user_id=1011185293)
    for item in vbn:
        #print(item.result)
        print(f"Режим - {item.user_command}\nЗапрос - {item.user_search}\nДата и время запроса - {item.datetime_search}")
