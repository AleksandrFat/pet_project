import requests
import json
from time import sleep
from random import choice
from datetime import datetime

url = 'https://roscarservis.ru/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&set_filter=Y&sort%5Brecommendations' \
      '%5D=asc&PAGEN_1=1'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
host_url = 'https://roscarservis.ru'


def get_data_json_all_items(url, headers):
    # все наши json файлы на всех страницах и будем отдельно их обробатывать
    start = datetime.now()
    data_json = []
    response = requests.get(url, headers=headers)
    page_count = response.json()['pagesCount']
    pause_list = [1, 2, 3, 4]
    for page in range(1, page_count + 1):
        print(f'Забмраем с сайта json файл. Страница {page} из {page_count} ')
        r = requests.get(response.url[:-1] + str(page), headers=headers)
        data_json.append(r.json())
        if page == page_count:
            end = datetime.now()
            work_time = end - start
            print(f'Завершение сбора даных... Время сборра данных: {work_time} мс.')
        else:
            pause = choice(pause_list)
            print(f'Делаем паузу в {pause} секунды.')
            sleep(pause)
    return data_json


def get_result(data):
    print('-' * 20)
    print('Формируем список для записи в json файл...')
    result = []
    for i in data:
        for item in i['items']:
            tmp = {}
            tmp['Наименование'] = item['name']
            tmp['Цена за одну позицию в рублях'] = item['price']
            tmp['Цена за комплект (4 шт.) в рублях'] = item['price'] * 4
            tmp['Всего товара доступно'] = item['amount']
            tmp['Ссылка на изображение товара'] = host_url + item['imgSrc']
            tmp['Ссылка на сам товар'] = host_url + item['url']
            result.append(tmp)
    return result


def get_json(data):
    name = f'Pars from {datetime.now().date().strftime("%d.%m.%Y")}.json'
    with open(name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=3, ensure_ascii=False)
    print('-' * 20)
    print('Работа завершена!')


# Вызов для получения json!!!
data_items = get_data_json_all_items(url, headers=headers)

# Формируем список result для записи в json файл
rusult_json = get_result(data_items)

# Запись данных в json файл
get_json(rusult_json)
