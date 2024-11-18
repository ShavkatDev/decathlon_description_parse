import requests
import json
import csv
import os
import getpass

filename = 'cody/csvs/login.csv'

def save_credentials(login, password):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'password'])
        writer.writerow([login, password])
    print("Данные успешно сохранены.")

def load_credentials():
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            credentials = next(reader, None)
            if credentials:
                return credentials
    return None

def get_credentials():
    credentials = load_credentials()
    if credentials:
        print("Используем сохраненные данные.")
        return credentials
    else:
        login = input("Введите логин: ")
        password = getpass.getpass("Введите пароль: ")
        save_credentials(login, password)
        return [login, password]

bearer_token = 'eyJraWQiOiJidXNpbmVzcyIsImFwcCI6ODQsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJDT0RZIiwiaWF0IjoxNzE4MzU4MDk2LCJleHAiOjE3NDk5MTUwNDgsIndpZCI6ODEsImlkeCI6ImJhY2tvZmZpY2UiLCJqdGkiOiJjMzAyMTAyYi04ZmQyLTRhZDMtYjY1Ny03ZmExZDZhZmI1ZGQiLCJzY29wZXMiOiJwdWJsaWMgYWxsIn0.gNBv_Sk3KZoU1Kam-8er1oRb4bCd3PlljuC-eTsdtL8U6x5lHTxrdP6b24ryvfdVUg_4f_WJMqP9TlVxNJ2-w61ekef83HxQ_xEecMI1C23ARLtbZYFCsyyhZAMx2FmM4df1HJHDMJStddgI_iq8reie2lLkamWWhK-Q8b5S0mMb4WIC1WAUa_FBToN8mTHrCVRehrp518a_pAMddB-JjL8DAqxHObqDS8RCDDi0DfPbnA4GGgLh8VsH1GeHaBGjBHD-e0LCxWF8zmRMs-CdHh67bHaz6Z7QIouaq9Sno27LW2YfHMSVPQbR0pKs3QHk90dp196Fanx7CngO1tMP0w'

headers_login = {
            "Authorization": "Basic YnVzaW5lc3M6YzQ5TmFlTlBRdThGZVQ3NDVhYlBDN2RiTTdqQk52N1A=",
            'Content-Type': 'application/json',
            "origin": "https://business.cody.mn",
            "priority": "u=1, i",
            "referer": "https://business.cody.mn/",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

def write_tokens_to_csv(access_token, refresh_token, filename='cody/csvs/tokens.csv'):
    tokens_data = [{'token_type': 'access', 'token': access_token}, {'token_type': 'refresh', 'token': refresh_token}]
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['token_type', 'token']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for token_data in tokens_data:
            writer.writerow(token_data)
    print(f'Токен успешно записан {filename}')

def authorization(): 
    url_check_email = 'https://api.cody.mn/graphql'
    headers_check_email = {'accept': '*/*', 'accept-language': 'en', 'content-type': 'application/json', 'origin': 'https://business.cody.mn', 'referer': 'https://business.cody.mn/', 'Authorization': 'Bearer eyJraWQiOiJidXNpbmVzcyIsImFwcCI6ODQsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJDT0RZIiwiaWF0IjoxNzE4MzU4MDk2LCJleHAiOjE3NDk5MTUwNDgsIndpZCI6ODEsImlkeCI6ImJhY2tvZmZpY2UiLCJqdGkiOiJjMzAyMTAyYi04ZmQyLTRhZDMtYjY1Ny03ZmExZDZhZmI1ZGQiLCJzY29wZXMiOiJwdWJsaWMgYWxsIn0.gNBv_Sk3KZoU1Kam-8er1oRb4bCd3PlljuC-eTsdtL8U6x5lHTxrdP6b24ryvfdVUg_4f_WJMqP9TlVxNJ2-w61ekef83HxQ_xEecMI1C23ARLtbZYFCsyyhZAMx2FmM4df1HJHDMJStddgI_iq8reie2lLkamWWhK-Q8b5S0mMb4WIC1WAUa_FBToN8mTHrCVRehrp518a_pAMddB-JjL8DAqxHObqDS8RCDDi0DfPbnA4GGgLh8VsH1GeHaBGjBHD-e0LCxWF8zmRMs-CdHh67bHaz6Z7QIouaq9Sno27LW2YfHMSVPQbR0pKs3QHk90dp196Fanx7CngO1tMP0w', 'sec-ch-ua': '\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '\"Windows\"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    if not os.path.exists('cody/csvs'):
        os.makedirs('cody/csvs')
    credentials = get_credentials()
    email_cody = credentials[0]
    password_cody = credentials[1]
    data_check_email = {'operationName': 'authCheckLogin', 'variables': {'login': f'{email_cody}'}, 'query': '\n        mutation authCheckLogin($login: String!) {\n            exists: authCheckLogin(input: {login: $login})\n        }\n        '}
    response_check_email = requests.post(url_check_email, headers=headers_check_email, json=data_check_email)
    if response_check_email.ok:
        url_login = 'https://api.cody.mn/oauth/token'
        data_login = {'scope': 'public all', 'username': f'{email_cody}', 'password': f'{password_cody}', 'grant_type': 'password'}
        response_login = requests.post(url_login, headers=headers_login, json=data_login)
        if response_login.status_code != 200:
            print('[!] Неверный логин или пароль [!]\n')
            os.remove('cody/csvs/login.csv')
        if response_login.ok:
            print('Авторизация успешна!')
            response_data = response_login.json()
            token = response_data.get('access_token')
            refresh_token = response_data.get('refresh_token')
            write_tokens_to_csv(token, refresh_token)
            if token:
                headers_protected = headers_login.copy()
                headers_protected['Authorization'] = f'Bearer {token}'
                return headers_protected
        else:
            print('Ошибка при авторизации:', response_login.status_code, response_login.text)
    else:
        print('Ошибка при проверке email:', response_check_email.status_code, response_check_email.text)

def get_auth():
    url = 'https://api.cody.mn/graphql'
    payload = json.dumps({'operationName': 'me', 'variables': {}, 'query': 'query me {\n  me {\n    id\n    firstName\n    lastName\n    avatar\n    login\n    roles\n    email\n    mobile\n    roleMatrix\n    __typename\n  }\n}'})
    headers_protected = headers_login.copy()
    if not os.path.exists('cody/csvs/tokens.csv'):
        headers_protected = authorization()
    else:
        with open('cody/csvs/tokens.csv', mode='r') as file:
            reader = csv.DictReader(file)
            tokens = [row for row in reader]
            headers_protected['Authorization'] = f'Bearer {tokens[0]["token"]}'
    response = requests.request('POST', url, headers=headers_protected, data=payload)
    if response.status_code != 200:
        print('Токен просрочен, обновляем....\n')
        os.remove('cody/csvs/tokens.csv')
        return get_auth()
    print('[#] Авторизация успешна!')
    
    return headers_protected