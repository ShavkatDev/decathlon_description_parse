import os
import csv
import time
import requests

from config import URL_SEARCH, URL_GET_INFO, HEADERS

def read_csv():
    result_list = []

    with open('skus.csv', 'r', encoding='utf-8', newline='\n') as file:
        reader = csv.DictReader(file)

        for sku in reader:
            result_list.append(sku['sku'])

    return result_list

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
            time.sleep(100)
    except:
        not_found_counter += 1
        print(f'[!] Not found [{search_sku}] [!]')

    for product in products:
        try:
            dsm_code = product['models'][0]['dsm_code']
        except:
            print(f'[!] Failed to get *dsm_code* [{search_sku}] [!]')

    response_get_info = requests.request('GET', URL_GET_INFO.format(dsm_code), headers=HEADERS)
    result_get_info = response_get_info.json()

    components = result_get_info['data']['components']

    for i in components:
        print(i)


def execute_script():
    counter = 1
    skus_list = read_csv()

    for sku in skus_list:
        if counter % 15 == 0:
            print(f'\n[#] Pause for 5 seconds... [#]\n')
            time.sleep(5)

        search_item(sku)
        print(f'[#] {counter}. {sku} - OK [#]')
    
        counter += 1

def main():
    print('[#] Запуск скрипта! [#]')    

    execute_script()

    print('[#] Скрипт закончен! [#]')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[!] Скрипт остановлен [!]")