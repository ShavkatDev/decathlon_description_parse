import os
import csv
import time
import json
import requests

from googletrans import Translator

from config import URL_SEARCH, URL_GET_INFO, HEADERS

translator = Translator()

def add_data_to_json(new_data, file_path='data_ru.json'):
    try:
        # Чтение существующих данных из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не существует или пуст, создаем пустой список для данных
        data = []

    # Добавление новых данных
    for i in new_data:
        data.append(i)

    # Запись обновленных данных в файл
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def read_csv():
    result_list = []

    with open('skus.csv', 'r', encoding='utf-8', newline='\n') as file:
        reader = csv.reader(file, delimiter=',')

        for row in reader:
            result_list = row.copy()

    result_list_uniq = list(set(result_list))

    return result_list_uniq

def search_item(search_sku):
    not_found_counter = 0

    response = requests.request('GET', URL_SEARCH.format(search_sku), headers=HEADERS)
    try:
        result = response.json()
    except:
        print(f'[!] Status code: {response.status_code}, Response Text: {response.text} [!]')
    products = ''

    try:
        products = result['data']['products']
        if len(products) > 1:
            print('[#] More Variants than 1')
    except:
        not_found_counter += 1
        print(f'[!] Not found [{search_sku}] [!]')
        return False
    
    if not products:
        print(f'[!] Failed with products - [{search_sku}] [!]')


    for product in products:
        try:
            dsm_code = product['models'][0].get('dsm_code')
        except:
            print(f'[!] Failed to get *dsm_code* [{search_sku}] [!]')

    response_get_info = requests.request('GET', URL_GET_INFO.format(dsm_code), headers=HEADERS)
    
    #Проверка
    if response_get_info.status_code == 200:
        result_get_info = response_get_info.json()
    else:
        print(f'[#] Error with request - {response_get_info.status_code} in second request')
        
        return False

    components = result_get_info['data']['components']

    benefits_components=''
    functionality_components=''
    composition_components=''

    for i in components:
        if i['type'] == 'benefits':
            benefits_components = i['contents']
        elif i['type'] == 'functionality':
            functionality_components = i['contents']
        elif i['type'] == 'composition':
            composition_components = i['content']
    
    return {'sku': search_sku, 'dsm_code': dsm_code, 'benefits_components': benefits_components, 'functionality_components': functionality_components, 'composition_components': composition_components}
    
def execute_script():
    counter = 1
    skus_list = read_csv()

    components = []

    for sku in skus_list:
        components.append(search_item(sku))
        if not components:
            continue
        if counter % 15 == 0:
            print(f'\n[#] Pause for 5 seconds... [#]\n')
            add_data_to_json(components)
            components=[]
            time.sleep(5)
        counter += 1

        print(f'[{counter}/3665] - Success')

def translate_json(data):
    if isinstance(data, dict):  # Если словарь
        translated = {}
        for key, value in data.items():
            if key in {'image_url', 'sku', 'dsm_code'}:
                translated[key] = value  # Оставляем как есть
            else:
                translated[key] = translate_json(value)  # Рекурсия
        return translated
    elif isinstance(data, list):  # Если массив
        return [translate_json(item) for item in data]  # Рекурсия
    elif isinstance(data, str):  # Если строка
        # Перевод строки
        translated_text = translator.translate(data, src='zh-cn', dest='ru').text
        return translated_text
    else:  # Если другое (число, None и т.д.)
        return data

def translate_to_ru():

    data_ru = []
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    counter = 1
    for i in data:
        if counter % 15 == 0:
            add_data_to_json(data_ru)
        try:
            translated_json = translate_json(i)
            data_ru.append(translated_json)
            print(f'[#{counter}#] Succesfully translated [{i['sku']}]')
        except Exception as ex:
            print('[!] Error with translate:\n', ex)
        
        counter += 1

        

        # sku=i['sku']
        # dsm_code=i['dsm_code']
        # benefits_components=i['benefits_components']
        # functionality_components=i['functionality_components']
        # composition_components=i['composition_components']

        # benefits_components_ru=''
        # if benefits_components:
        #     benefit_ru = []
        #     for benefit in benefits_components:
        #         benefit_text = translator.translate(benefit['text'], src='zh-cn', dest='ru').text.capitalize()
        #         benefit_titile = translator.translate(benefit['title'], src='zh-cn', dest='ru').text.capitalize()
        #         benefit_image = benefit['image_url']

        #         benefit_ru.append({'text': benefit_text, 'title': benefit_titile, 'image_url': benefit_image, })
            
        #     benefits_components_ru = {'benefits_components': benefit_ru}
        
        # functionality_components_ru=''
        # if functionality_components:
        #     functionality_ru = []
        #     for functional in functionality_components:
        #         functional_text = translator.translate(functional['text'], src='zh-cn', dest='ru').text.capitalize()
        #         functional_titile = translator.translate(functional['title'], src='zh-cn', dest='ru').text.capitalize()

        #         functionality_ru.append({'text': functional_text, 'title': functional_titile})
            
        #     functionality_components_ru = {'functionality_components': functionality_ru}
        
        # if composition_components:
        #     composition_ru = []
        #     if composition_components.get('composition_map'):
        #         print(composition_components.get('composition_map'))
        #     else:
        #         print(0)


        # data_ru.append({'sku': sku, 'dsm_code': dsm_code, 'benefits_components': benefits_components_ru, 'functionality_components': functionality_components_ru, 'composition_components': composition_components_ru})



    # Перевод с русского на узбекский (REALIZE LATER)
    # translated_to_uzbek = translator.translate(translated_to_russian.text, src='ru', dest='uz')
    # print("Перевод на узбекский:", translated_to_uzbek.text)




def main():
    print('[#] Запуск скрипта! [#]')    

    # Эта функция запускает парсер для Decathlon.
    # execute_script()

    # Эта функция для четния и дальнейшего перевода json
    translate_to_ru()

    print('[#] Скрипт закончен! [#]')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[!] Скрипт остановлен [!]")