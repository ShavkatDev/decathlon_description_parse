import json
import csv

URL = 'https://api.cody.mn/graphql'
GET_DESCRIPTION_PAYLOAD = {
    "operationName": "product",
    "variables": {
        "id": ""
    },
    "query": "query product($id: ID!) {\n  product(id: $id) {\n    id\n    name(locale: \"all\")\n    currentName: name\n    image\n    title(locale: \"all\")\n    description(locale: \"all\")\n    availableOn\n    availableUntil\n    slug\n    sku\n    productCat\n    storeId\n    shippingCategoryId\n    condition\n    cancelDuration\n    info\n    sizingGuideId\n    currency\n    createdAt\n    updatedAt\n    vendor {\n      name\n      __typename\n    }\n    __typename\n  }\n}"
}

def read_csv():
    with open('skus.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            unique_elements = list(set(row))
            return unique_elements
        
def read_json():
    file_path = "data_original.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    skus_list = []
    for sku in data:
        if sku:
            skus_list.append(sku['sku'])

    unique_elements = list(set(skus_list))

    return unique_elements