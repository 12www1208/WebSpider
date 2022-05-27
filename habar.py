from bs4 import BeautifulSoup
import requests
import json

def habrParser(a):
    page = 1
    parser = []
    for i in range(a):
        url = requests.get(f'https://habr.com/ru/news/page{page}')

        html = BeautifulSoup(url.text, 'html.parser')

        blokNews = html.find_all('article', class_='tm-articles-list__item')

        for news in blokNews:
            name = news.find('a', class_='tm-article-snippet__title-link').text
            data = (news.find('time')).get('title')
            how = news.find('a', class_='tm-user-info__username').text
            view = news.find('span', class_='tm-icon-counter__value').text
            link = 'https://habr.com' + (news.find('a', class_='tm-article-snippet__title-link')).get("href") 

            parser.append(
                {
                    'article': name,
                    'dataPost': data,
                    'User': how,
                    'views': view,
                    'links': link
                }
            )
        page += 1
    print(parser)
    with open('parser.json', 'w') as file:
       json.dump(parser, file, indent=4, ensure_ascii=False)

