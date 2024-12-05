from register import get_auth
from get_description import get_id, description
from config import read_json
from get_auth_translate import get_iam
from save_files import load_processed_skus, save_processed_skus

def main():
    headers = get_auth()
    skus_list = read_json()

    processed_skus = load_processed_skus("files/processed_skus.txt")

    skus_lenght = len(skus_list) - len(processed_skus)
    buffer = []
    
    counter = 1
    IAM_TOKEN = get_iam()
    for sku in skus_list:
        if sku not in processed_skus:
            result = description(headers, get_id(headers, sku), IAM_TOKEN)

            if result[0] != 200:
                print(f'[{counter}/{skus_lenght}] Error with {sku}:\n{result[1]}')
            elif result[0] == 101:
                print(f'[{counter}/{skus_lenght}] Success without changing description {sku}')
            else:
                print(f'[{counter}/{skus_lenght}] Success with {sku}')
        
            buffer.append(sku)

            if len(buffer) == 10:
                save_processed_skus(buffer, "files/processed_skus.txt")
                processed_skus.update(buffer)
                buffer = []
        else: print(f'[{counter}/{skus_lenght}] Already changed {sku}')
        counter+=1

    if buffer:
        save_processed_skus(buffer, "files/processed_skus.txt")

if __name__ == '__main__':
    main()