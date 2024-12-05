import os
import csv
import time
import json
import urllib3
import requests

from googletrans import Translator
import urllib3.connection

from config import URL_SEARCH, URL_GET_INFO, HEADERS
from register import get_auth
from change_description import get_id, load_description

translator = Translator()

def add_data_to_json(new_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(new_data, file, indent=4)

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

    with open('data.json', 'r') as file:
        data = json.load(file)
    
    counter = 1
    data_ru = []
    for i in data:
        if counter <= 3390:
            counter += 1
            continue
        try:
            translated_json = translate_json(i)
            data_ru.append(translated_json)
            print(f'[#{counter}#] Успешно переведено [{i['sku']}]')
        except Exception as ex:
            print('[!] Ошибка с переводом:\n', ex)
        
        if counter % 10 == 0:
            add_data_to_json(data_ru, file_path=f'files/data_ru_{counter}.json')
            data_ru = []
            print(f'[#] Записано в data_ru.json [#]')
        
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

def read_construct():
    description = []
    counter = 1
    for file_name in os.listdir('files'):
        file_path = os.path.join('files', file_name)
        if os.path.isfile(file_path):  # Проверяем, что это файл
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                parsed_data = json.loads(content)
                for i in parsed_data:
                    constructed_description = ''
                    benefits_components = i['benefits_components']
                    functionality_components = i['functionality_components']
                    composition_components = i['composition_components']
                    if benefits_components:
                        benefit_description = """
                                <h2>Функции</h2><div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 800px; margin: 0;">
                                """
                        for benefit in benefits_components:
                            benefits_title = benefit.get('title') or ''
                            benefits_text = benefit.get('text') or ''
                            image = benefit['image_url']  or ''
                            benefit_description+=f"""
                                <div style="padding: 10px; box-sizing: border-box; display: flex; align-items: flex-start; gap: 10px;">
                                    <img src="{image}" alt="{benefits_title.capitalize()}" style="width: 56px; height: 56px; flex-shrink: 0;">
                                    <div>
                                        <h4 style="margin: 0 0 5px; font-size: 16px;">{benefits_title.capitalize()}</h4>
                                        <p style="margin: 0; font-size: 14px; color: #555;">{benefits_text.capitalize()}</p>
                                    </div>
                                </div>
                                """
                        benefit_description += '</div>'
                        constructed_description += benefit_description                           
                    
                    if functionality_components:
                        functionality_description = '<div><h2>Советы по эксплуатации</h2>'
                        for functional in functionality_components:
                            functional_title = functional['title'].capitalize()
                            functional_text = functional['text'].capitalize()
                            functionality_description += f"<h4 style='margin: 0px'>{functional_title}</h4><p style='margin: 0px'>{functional_text}</p>"

                        constructed_description += functionality_description

                    if composition_components:
                        composition_description = '<h2>Технические характеристики</h2>'
                        for key, value in composition_components.items():

                            for key, value in composition_components.items():
                                if key == 'storage_advice' and value:
                                    composition_description += f'<h4 style="margin: 0px">Рекомендации по хранению</h4>' + f"<p style='margin: 0px'>{value}</p>"
                                elif key == 'approved_by' and value:
                                    composition_description +=f'<h4 style="margin: 0px">Сертификат</h4>' + f"<p style='margin: 0px'>{value}</p>"
                                elif key == 'composition_map' and value:
                                    composition_description += f'<h4 style="margin: 0px">Материал</h4>' + f"<p style='margin: 0px'>{value}</p>"
                                elif key == 'use_restriction' and value:
                                    composition_description += f'<h4 style="margin: 0px">Инструкция по применению</h4>' + f"<p style='margin: 0px'>{value}</p>"
                                elif key == 'lab_tests' and value:
                                    composition_description += f'<h4 style="margin: 0px">Тестирование</h4>' + f"<p style='margin: 0px'>{value}</p>"
                        
                        constructed_description += composition_description + '</div>'

                    description.append({'sku': i['sku'], 'description': '<div>'+constructed_description+'</div>'})
                    if counter <= 20 and counter % 2 == 0:
                        with open(f'html_test/page_{counter}.html', 'w',encoding='utf-8') as file:
                            file.write(constructed_description)
                    print(f'[#{counter}] - Success! [###]]')
                    counter+=1

    with open('csv_filename.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['sku', 'description'])
        writer.writeheader()  # Записываем заголовки
        writer.writerows(description)  # Записываем данные

def read_csv():
    with open('unique_sku.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        result = []
        for row in reader:
            result.append({'sku': row['sku'], 'description': row['description']})

    return result      

def main():
    print('[#] Запуск скрипта! [#]')    

    # Эта функция запускает парсер для Decathlon.
    # execute_script()

    # Эта функция для четния и дальнейшего перевода json
    # translate_to_ru()

    # Эта функция для чтения csv
    # result = read_construct()

    # Добавление описания
    headers = get_auth()
    result_csv = read_csv()
    counter = 1
    for i in result_csv:
        if counter <= 3059:
            counter+=1
            continue
        if counter % 200 == 0:
            headers = get_auth()
            time.sleep(10)
        if counter % 15 == 0:
            print('[###] - Pause 5 seconds...[###]')
            time.sleep(5)
        
        try:
            id = get_id(headers, i['sku'])
            if 'Функции' in i['description'] or 'Советы по эксплуатации' in i['description']:
                print(f'[#{counter}] - Already uploaded - [{i['sku']}]/[{id}]')
                counter+=1
                continue
            status_code = load_description(headers, id, i['description'])
            if status_code[0] == 200:
                print(f'[#{counter}] - Success! - [{i['sku']}]/[{id}]')
            else:
                print(f'[#############]\n[!!!]{i['sku']}[!!!]\n[!!!]  {status_code[0]}  [!!!]\n[#############]\n\n')

        except urllib3.connection.ConnectionError:
            print('Time sleep due to error')
            time.sleep(15)
        
        counter+=1

    print('[#] Скрипт закончен! [#]')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[!] Скрипт остановлен [!]")