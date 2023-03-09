import requests
from time import sleep
import xlsxwriter
url = 'https://www.autosklad31.ru/shop/products/selected/42/set/174;214;336;266;158;159;607/?offset=0&limit=12' \
      '&orphans=0&order_by=name_asc&display_as=tiled&format=json&cache_id=27969666'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',

}
base_url = 'https://www.autosklad31.ru/'


def get_url_json(url, headers):
    response = requests.get(url, headers=headers)
    total_count = response.json()['meta']['total_count']
    data_json = []
    for offset in range(0, total_count, 12):
        sleep(2)
        print(f'Забираем данные со страницы № {len(data_json) + 1} / {total_count // 12 + 1}')
        scr = f'https://www.autosklad31.ru/shop/products/selected/42/set/174;214;336;266;158;159;607/?offset={offset}&limit=12' \
              '&orphans=0&order_by=name_asc&display_as=tiled&format=json&cache_id=27969666'
        r = requests.get(scr, headers=headers)
        data_json.append(r.json())
    print('Сбор закончен...')
    return data_json


def data_writer(data_json):
    data_writer = []
    print('Форимируем данные для записи...')
    sleep(2)
    for item in data_json:
        for product in item['objects']:
            name_product = product['name'].strip()
            price_product = product['price']
            src_price = base_url + product['resource_uri']
            data_writer.append((name_product, price_product, src_price))
    return data_writer


def writer_file(parametr):
    print('Записываем данные в файл...')
    workbook = xlsxwriter.Workbook('data_transmission.xlsx')
    worksheet = workbook.add_worksheet('Товар')

    bold = workbook.add_format({'bold': True})

    money = workbook.add_format({'num_format': '#,##0 руб'})

    worksheet.set_column('A:A', 60)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 100)
    worksheet.write('A1', 'Наименование товара', bold)
    worksheet.write('B1', 'Цена товара в рублях', bold)
    worksheet.write('C1', 'Ссылка на товар', bold)

    row = 1
    col = 0

    for item in parametr:
        worksheet.write(row, col, item[0])
        worksheet.write(row, col + 1, item[1], money)
        worksheet.write(row, col + 2, item[2])
        row += 1
    workbook.close()


#  Забираем json со всех наших страниц
data_json = get_url_json(url, headers=headers)

#  Ищем необходимую информацию
data_writer = data_writer(data_json)

#  Сортируем по цене
data_writer = sorted(data_writer, key=lambda item: item[1])

# Записывваем наши данные в xlsx файл
writer_file(data_writer)
