from dotenv import find_dotenv, load_dotenv
import os


load_dotenv(find_dotenv())


keys_actor: tuple = ('birthDate', 'birthPlace', 'heightCentimeters', 'realName')
keys: tuple = ('title', 'url', 'runningTimeInMinutes', 'titleType', 'rating', 'year', 'genres', 'text')
keys_for_top: tuple = ('runningTimeInMinutes',  'year')
keys_role: tuple = ('Actor', 'Actress', 'Producer')


button_translate: tuple = ('English', 'German', 'Русский', 'Spanish', 'Italian', 'Turkish', 'Japanese', 'Chinese (Simplified)')
button_film: tuple = ('Повторить поиск Фильма', 'Перейти в меню')
button_actor: tuple = ('Посмотреть фильмографию', 'Повторить поиск Актера')
button_top_first: tuple = ('Боевик', 'Биографический', 'Вестерн', 'Военный', 'Драма',
                    'Детектив', 'Исторический', 'Комедия', 'Мультфильмы', 'Мистика', 'Другие жанры ->')
button_top_second: tuple = ('Мюзикл', 'Музыкальный', 'Научная фантастика', 'Нуар',
                            'Приключения', 'Семейный', 'Спорт', 'Триллер', 'Ужасы', 'Фэнтази', '<- Предыдущие')
button_top_limit: tuple = ('10', '20', '50', '100')


dict_translate: dict = {
    'English': 'en', 'German': 'de', 'Русский': 'ru',
    'Spanish': 'es', 'Italian': 'it', 'Turkish': 'tr',
    'Japanese': 'ja', 'Chinese (Simplified)': 'zh'
}
dict_top: dict = {
    'Боевик': 'action', 'Приключения': 'adventure', 'Мультфильмы': 'animation',
    'Биографический': 'biography', 'Комедия': 'comedy', 'Детектив': 'crime',
    'Драма': 'drama', 'Семейный': 'family', 'Фэнтази': 'fantasy', 'Нуар': 'film - noir',
    'Исторический': 'history', 'Ужасы': 'horror', 'Музыкальный': 'music',
    'Мюзикл': 'musical', 'Мистика': 'mystery', 'Романтика': 'romance', 'Научная фантастика': 'sci - fi',
    'Спорт': 'sport', 'Триллер': 'thriller', 'Военный': 'war', 'Вестерн': 'western'
            }


headers_imdb: dict = {
    "X-RapidAPI-Key": os.getenv('X-RapidAPI-Key_imdb'),
    "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
}
headers_translate: dict = {
    "content-type": "application/x-www-form-urlencoded",
    "X-RapidAPI-Key": os.getenv('X-RapidAPI-Key_translate'),
    "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
}


if __name__ == '__main__':
    print(dict_top.keys())