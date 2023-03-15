import requests
import os
from dotenv import find_dotenv, load_dotenv
from bot_admin.other_data import headers_translate


load_dotenv(find_dotenv())


def translate(in_lang: str, out_lang: str, new_text: str) -> str:
    """
    функция - парсинг переводчик
    :param in_lang: язык с которого требуется перевод
    :param out_lang: язык на который требуется перевод
    :param new_text: текст для перевода
    :return: строка перевода
    """
    response = requests.Session()
    text = '%' + new_text.encode(encoding='utf-8').hex('%')
    payload = f"source_language={in_lang}&target_language={out_lang}&text={text}"
    answer = response.post(os.getenv('url_translate'), data=payload, headers=headers_translate)
    return answer.json()['data']["translatedText"]


if __name__ == '__main__':
    text_1 = 'Christopher Lloyd'
    text_2 = 'кристофер ллойд'
    f_1 = translate(in_lang='en', out_lang='ru', new_text=text_1)
    f_2 = translate(in_lang='ru', out_lang='en', new_text=text_2)
    print(f_1)
    print(f_2)
