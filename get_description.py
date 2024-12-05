import json
import requests

from edit_html import translate_cyrillic_in_html, clean_html
from config import URL, GET_DESCRIPTION_PAYLOAD

def get_id(headers, sku):

    PAYLOAD = {
        "operationName": "GetVendorProduct",
        "variables": {
            "offset": 0,
            "first": 20,
            "filter": {
                "variantsIncludingMaster": {
                    "sku": {
                        "start": f"{sku}"
                    }
                }
            },
            "sort": {
                "field": "createdAt",
                "direction": "desc"
            },
            "businessId": "48510"
        },
        "query": "query GetVendorProduct($first: Int, $offset: Int, $filter: ProductFilter, $sort: SortFilter, $businessId: ID!) {\n  vendor(id: $businessId) {\n    id\n    products(first: $first, offset: $offset, filter: $filter, sort: $sort) {\n      totalCount\n      nodes {\n        id\n        currency\n        id\n        brand {\n          id\n          name\n          __typename\n        }\n        image(size: mini, mirror: false)\n        sku\n        name\n        merchantSku\n        sellingPrice\n        taxCode\n        packageCode\n        labelCode\n        barcode\n        slug\n        nameZh: name(locale: \"zh\")\n        nameRu: name(locale: \"ru\")\n        nameUz: name(locale: \"uz\")\n        nameMn: name(locale: \"mn\")\n        title\n        listings {\n          website {\n            id\n            name\n            __typename\n          }\n          __typename\n        }\n        totalOnHand\n        canSupply\n        keyword {\n          id\n          name\n          mn\n          __typename\n        }\n        productCat\n        price\n        availableOn\n        metaTitle\n        metaKeywords\n        metaDescription\n        fragile\n        nonReturnable\n        createdAt\n        updatedAt\n        sizingGuide {\n          id\n          title\n          gender\n          ageGroup\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }

    response = requests.post(URL, data=json.dumps(PAYLOAD), headers=headers)
    result = response.json()

    if result['data']['vendor']['products']['nodes']:
        return result['data']['vendor']['products']['nodes'][0]['id']

def description(headers, id, IAM_TOKEN):
    send_id = GET_DESCRIPTION_PAYLOAD
    send_id['variables']['id'] = id
    try:
        response = requests.post(URL, data=json.dumps(send_id), headers=headers)
    except:
        print(f'Error with request {id}')

    result = response.json()
    if "errors" in result:
        return [999, False]
    
    description_old = json.loads(result['data']['product']['description'])

    product = result['data']['product']
    # Обновляем описание

    #Очищаем от дублирования
    clean_description = clean_html(description_old["en"])
    if clean_description != description_old["en"]:
        description_old["en"] = clean_description
        description_old["ru"] = clean_description
        #Перевод с yandex translate
        description_old["uz"] = translate_cyrillic_in_html(clean_description, IAM_TOKEN)
    else:
        return [101, True]

    # Преобразуем `description_old` обратно в строку JSON
    product['description'] = json.dumps(description_old, ensure_ascii=False)
    product['condition'] = 'default'

    # Удаляем ненужные поля
    fields_to_remove = [
        'createdAt', 'currency', 'currentName', 'image', 'info',
        'shippingCategoryId', 'updatedAt', 'vendor', '__typename'
    ]
    for field in fields_to_remove:
        product.pop(field, None)

    # Преобразуем `product` в JSON-строку
    json_string = json.dumps(product, ensure_ascii=False)
    payload_load = {
        "operationName": "UpdateProductGeneral",
        "variables": json.loads(json_string),
        "query": "mutation UpdateProductGeneral($id: ID!, $name: String, $sku: String, $description: String, $slug: String, $title: String, $productCat: ProductCat, $availableOn: ISO8601DateTime, $availableUntil: ISO8601DateTime, $storeId: ID, $shippingCategoryId: ID, $condition: String, $cancelDuration: Int, $sizingGuideId: ID, $info: JSON, $currency: String, $fragile: Boolean, $nonReturnable: Boolean) {\n  product: updateProduct(\n    input: {id: $id, name: $name, sku: $sku, description: $description, slug: $slug, title: $title, productCat: $productCat, availableOn: $availableOn, availableUntil: $availableUntil, storeId: $storeId, shippingCategoryId: $shippingCategoryId, condition: $condition, cancelDuration: $cancelDuration, sizingGuideId: $sizingGuideId, info: $info, currency: $currency, fragile: $fragile, nonReturnable: $nonReturnable}\n  ) {\n    id\n    name\n    slug\n    sku\n    title\n    description\n    productCat\n    storeId\n    shippingCategoryId\n    condition\n    cancelDuration\n    availableOn\n    availableUntil\n    sizingGuideId\n    fragile\n    nonReturnable\n    info\n    __typename\n  }\n}"
    }

    response_load = requests.post(URL, data=json.dumps(payload_load), headers=headers)
    result_load = response_load.json()

    return [response_load.status_code, result_load]
    