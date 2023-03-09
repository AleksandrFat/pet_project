import requests
from bs4 import BeautifulSoup
from time import sleep

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36',
}


def dowload(url):
    with open('C:\\Users\\Алекандр\\Desktop\\pars\\pars_scrapingclub.com\\images\\' + url.split('/')[-1], 'wb') as file:
        response = requests.get(url, stream=True)
        for value in response.iter_content(1024 * 1024):
            file.write(value)


def get_url():
    for count in range(1, 8):
        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='col-lg-4 col-md-6 mb-4')
        print(f'pars page {count}')
        for i in data:
            card_url = 'https://scrapingclub.com' + i.find('a').get('href')
            yield card_url


def array():
    for card_url in get_url():
        response = requests.get(card_url, headers=HEADERS)
        sleep(1)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('div', class_='card mt-4 my-4')
        name = data.find('h3', class_='card-title').text
        price = data.find('h4').text
        text = data.find('p', class_='card-text').text
        url_img = 'https://scrapingclub.com' + data.find('img', class_='card-img-top img-fluid').get('src')
        dowload(url_img)
        yield name, price, text, card_url, url_img
