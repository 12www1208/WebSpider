from bs4 import BeautifulSoup
import requests
import json

def newsParser():
    parser = []

    url = requests.get('https://www.gazeta.ru/news/')
    html = BeautifulSoup(url.text, 'html.parser')
    newsAll = html.find_all('div', class_='b_ear m_techlisting')
    for news in newsAll:
        name = news.find('a').text
        date = news.find('time', class_='b_ear-time').text
        link = f'https://www.gazeta{(news.find("a")).get("href")}'

        parser.append(
            {
                'article': name,
                'dataPost': date,
                'links': link
            }
        )

        with open('parser.json', 'w') as file :
            json.dump(parser, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    newsParser()
