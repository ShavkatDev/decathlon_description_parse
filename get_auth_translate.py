import requests

def get_iam():
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = '{"yandexPassportOauthToken":"y0_AgAAAAAwGOA3AATuwQAAAAEIJgp5AADQlgpEiq9I8KekKyGpBEkSG9JMvA"}'.encode()
    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)
    result = response.json()
    
    print("[#] IAM-TOKEN UPDATED")
    return result['iamToken']
