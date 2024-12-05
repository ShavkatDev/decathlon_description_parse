import re
import time
import requests
from bs4 import BeautifulSoup

from get_auth_translate import get_iam

folder_id = 'b1gjpj47udtkl4lh7dv8'
source_language = 'ru'

# Регулярное выражение для поиска кириллического текста
CYRILLIC_PATTERN = re.compile(r"[А-Яа-яЁё]+")

def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Словарь для хранения встреченных заголовков
    seen_headers = {}

    # Находим все элементы в DOM
    elements = soup.find_all()

    # Флаг для удаления элементов после повторного заголовка
    delete_mode = False

    for element in elements:
        # Проверяем, является ли элемент заголовком h2 или h4
        if element.name in ['h2', 'h4']:
            header_text = element.get_text(strip=True)

            # Если этот заголовок уже встречался, активируем режим удаления
            if header_text in seen_headers:
                delete_mode = True
                element.decompose()  # Удаляем сам заголовок
                continue  # Переходим к следующему элементу

            # Если заголовок не встречался ранее, добавляем его в список
            seen_headers[header_text] = True

        # Если режим удаления активен, удаляем текущий элемент
        if delete_mode:
            element.decompose()

    cleaned_html = soup.prettify()
    return cleaned_html

# Функция для перевода текста
def translate_text(text, IAM_TOKEN):
    
    if not text.strip():
        return text

    target_language = 'uz'
    texts = [text]

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )

    
    if response.status_code != 200:
        print('Error, wait for 20 seconds!')
        time.sleep(20)
    elif response.status_code == 401:
        IAM_TOKEN = get_iam()

    try:
        response_data = response.json()
    except Exception as ex:
        print(ex)
    return response_data.get('translations')[0].get('text')

def translate_cyrillic_in_html(html_content, IAM_TOKEN):
    soup = BeautifulSoup(html_content, "html.parser")

    # Рекурсивная функция для обработки текста в HTML
    def process_node(node):
        if node.name is None:  # Это текстовый узел
            # Проверяем, есть ли в тексте кириллица
            if CYRILLIC_PATTERN.search(node):
                original_text = node.strip()
                translated_text = translate_text(str(original_text), IAM_TOKEN)
                node.replace_with(translated_text)
        else:
            # Обходим дочерние элементы
            for child in node.contents:
                process_node(child)

    # Обрабатываем всё дерево
    process_node(soup)

    # Возвращаем обновлённый HTML
    return soup.prettify()

# translated_html = translate_cyrillic_in_html(html_content)
