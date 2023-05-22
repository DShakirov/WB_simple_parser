import requests
import json
import pandas as pd
import os
from time import strftime

def get_wb_catalogs_data():
    url = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru-v2.json'
    headers = {

        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Origin": "https://www.wildberries.ru",
        "Referer": "https://www.wildberries.ru/",
        "Sec-Ch-Ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    response = requests.get(url=url, headers=headers)
    data = response.json()
    with open('catalogs.json', 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def get_products_data(shard,query, wburl):
    result_list = []
    for page in range(1, 101):
        print (f'Отправлен запрос на страницу {page}')
        headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': f'https://www.wildberries.ru{wburl}?sort=popular&page={page}',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        }
        url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub&dest=-1257786&page={page}&regions=80,115,83,38,4,64,33,68,70,69,30,86,75,40,1,66,110,31,22,48,71,114&sort=popular&spp=0&{query}'
        response = requests.get(url=url, headers=headers)
        try:
            data = response.json()['data']['products']
        except:
            continue
        for product in data:
            try:
                price = int(product['priceU'])/100
            except:
                price = 0
            try:
                color = product['colors'][0]['name']
            except:
                color = ''
            try:
                sales_price = int(product['salePriceU'] / 100)
            except:
                sales_price = 0

                color = '0'
            result_list.append(
                {
                    "Наименование": product['name'],
                    "Бренд": product['brand'],
                    "Цена": price,
                    "Цена со скидкой": sales_price,
                    "Цвет": color,
                    "Ссылка": f'https://www.wildberries.ru/catalog/{product["id"]}/detail.aspx?targetUrl=BP',
                }
            )
        print(f"Данные со страницы {page} получены")

    if not os.path.exists('results'):
        os.mkdir('results')
    unix = str(strftime('[%d-%m-%Y]'))
    folder = f'results/{unix}'
    if not os.path.exists(folder):
        os.mkdir(folder)
    print('Путь к файлу результата создан')

    df = pd.DataFrame(data=result_list)
    file_name = f'{folder}/wb.csv'
    df.to_csv(file_name, mode='w', encoding='cp1251')
    print('Запись в файл успешна')

if __name__ == '__main__':
    shard = "autoproduct6"
    query = "subject=7749"
    wburl = "/catalog/avtotovary/kraski-i-gruntovki/kraski-aerozolnye"
    get_products_data(shard, query, wburl)

