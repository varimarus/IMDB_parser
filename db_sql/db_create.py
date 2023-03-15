from peewee import SqliteDatabase, Model
from peewee import IntegerField, TextField, CharField, DateTimeField, ForeignKeyField
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())
db = SqliteDatabase(
    os.path.join(os.getenv('path_db')),
    pragmas={'journal_mode': 'wal'}
)


class BaseModel(Model):  # Класс для создания экземпляра базы данных
    """
    Базовый класс создающий экземпляр существующей БД,
    наследование от Model ORM peewee
    """
    class Meta:
        database = db


class User(BaseModel):  # Класс для создания базы данных
    """
    Класс для создания таблици с основными данными о пользователе
     полученые в результате взаимодействия
    """
    telegram_id = IntegerField()
    user_name = TextField()
    user_command = CharField(max_length=15)
    user_search = TextField()
    datetime_search = DateTimeField()

    class Meta:
        """
        Класс для изменения имени таблицы в БД
        """
        db_table = 'Users'


class Movie(BaseModel):  # Класс для создания базы данных
    """
    Класс для создания таблици с данными о действие пользователя в рамках поиска фильмов
    """
    user_id = ForeignKeyField(User)
    request = TextField(User)
    result = TextField()

    class Meta:
        """
        Класс для изменения имени таблицы в БД
        """
        db_table = 'Search_movie'


class Actor(BaseModel):  # Класс для создания базы данных
    """
    Класс для создания таблици с данными о действие пользователя в рамках поиска актеров
    """
    user_id = ForeignKeyField(User)
    request = TextField(User)
    result = TextField()

    class Meta:
        """
        Класс для изменения имени таблицы в БД
        """
        db_table = 'Search_actor'


class Translate(BaseModel):  # Класс для создания базы данных
    """
    Класс для создания таблици с данными о действие пользователя в рамках переводчика
    """
    user_id = ForeignKeyField(User)
    request = TextField(User)
    result = TextField()


class Favorites(BaseModel):
    """
    Класс для создания таблици с данными о действие пользователя в рамках добавления в избранное
    """
    user_id = ForeignKeyField(User)
    request = TextField(User)
    result = TextField()


def create_database():
    db.create_tables([User, Movie, Actor, Translate, Favorites])
