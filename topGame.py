from bs4 import BeautifulSoup
import requests
import json

def topGame():
    parser = []

    for i in range(3):
        url = requests.get(f'https://stopgame.ru/review/new/izumitelno/p{i}')

        html = BeautifulSoup(url.text, 'html.parser')

        allBloks = html.find_all('div', class_ = 'item article-summary')

        for blok in allBloks:
            name = (blok.find('div', class_='caption caption-bold')).text  
            date = (blok.find('span', class_='info-item timestamp')).text
            links = 'https://stopgame.ru' + ((blok.find('a', class_='article-image image')).get('href'))
            coments = (blok.find('span', class_='info-item comments')).text

            parser.append(
                {
                    'article': name,
                    'dataPost': date,
                    'coments': coments,
                    'link': links
                }
            )
    print(parser)
    with open('parser.json', 'w') as f:
        json.dump(parser, f, indent=4, ensure_ascii=False)



if __name__ == '__main__':
    topGame()
