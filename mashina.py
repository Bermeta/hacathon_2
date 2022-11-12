from bs4 import BeautifulSoup
import requests 
import csv



count = 0

def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def get_data(html: str) -> bool:

    soup = BeautifulSoup(html, 'html.parser')
  
    catalog = soup.find('div',  class_ = 'search-results-table')

    if not catalog: 
        return False

    cars = catalog.find_all('a', class_ = 'list-item.list-label').get('href')

    for car in cars:
        model = cars.find('div', class_ = 'block title').text.strip()
        print(model)

        description = car.find('div', class_ = 'block info-wrapper item-info-wrapper').text
        if not description:
            description = 'Нет описания!'
        

        price = car.find('div', class_ = 'block price').text
        try:
            image = car.find('div', class_ = 'tmb-wrap-table').get('src') #get src to get url for image
        except:
            image = 'Нет картинки!'
        
        data = {
            'model': model,
            'description': description,
            'price': price, 
            'img': image
        }
        write_to_csv(data)
    return True


def write_to_csv(data: dict) -> None:

    global count  
    with open('mashina.csv', 'a') as file:
        fieldnames = ['№','Модель','Описание','Цена','Фото']
        writer = csv.DictWriter(file, fieldnames)
        count += 1
        writer.writerow({
            '№': count,
            'Модель': data.get('model'),
            'Описание': data.get('description'),
            'Цена': data.get('price'),
            'Фото': data.get('img')
        })
def prepare_csv()  -> None:

    with open('mashina.csv', 'w') as file:
        fieldnames = ['№','Модель','Описание','Цена','Фото']
        writer = csv.DictWriter(file, fieldnames)
        writer.writerow({
            '№': '№',
            'Модель': 'Модель',
            'Описание': 'Описание',
            'Цена': 'Цена',
            'Фото': 'Фото'
        })



def main():
    i = 1
    prepare_csv()
    while True:
        BASE_URL = f'https://www.mashina.kg/search/all/{i}'
        html = get_html(BASE_URL)
        is_res = get_data(html)
        if not is_res:
                break
    print(f'Страница: {i}')
    i += 1


main()
