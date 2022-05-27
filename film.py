from bs4 import BeautifulSoup
import requests
import json

def filmParser(a):
    parser = []
    for i in range(a):

        url = requests.get(f'https://www.kinoafisha.info/rating/movies/?page={i}')
        html = BeautifulSoup(url.text, 'html.parser')

        blokFilms = html.find_all('div', class_='movieItem-position')

        for blok in blokFilms:
            place = blok.find('span', class_='movieItem_position').text
            name = blok.find('a', class_="movieItem_title").text
            genres = blok.find('span', class_='movieItem_genres').text
            data = blok.find('span', class_='movieItem_year').text
            rating = blok.find('span', class_='rating_num').text
            img = blok.find('source', type="image/jpeg").get('srcset')
            link = blok.find('a', class_="movieItem_title").get('href')
            parser.append(
                {
                    'name': name,
                    'place': place,
                    'rating': rating,
                    'genres': genres,
                    'img': img,
                    'data': data,
                    'link': link
                }
            )
    with open('parser.json', 'w') as file:
        json.dump(parser, file, indent=4, ensure_ascii=False)


