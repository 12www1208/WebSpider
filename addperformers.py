import sqlite3
from bs4 import BeautifulSoup
import requests


def addMusikDB():
    connect = sqlite3.connect('databased.db', check_same_thread=False)

    cursor = connect.cursor()

    nameList = []
    linkLsit = []

    i = 0
    x = 0
   
    while True:
        url = requests.get(f'https://ru.hitmotop.com/artists/start/{x}')
        html =  BeautifulSoup(url.text, 'html.parser')

        bloks = html.find_all('li', class_='album-item')

        for blok in bloks:
            name = blok.find('span', class_='album-title').text
            link = 'https://ru.hitmotop.com' + blok.find('a', class_='album-link').get('href')
            nameList.append(name)
            linkLsit.append(link)
            print(name)


       
        x += 48

        if x == 1056:
            break


    while i < len(nameList):
        name1 = nameList[i]
        link1 = linkLsit[i]

        cursor.execute('INSERT INTO performers VALUES (?,?);', (name1, link1))
        connect.commit()
        print('Добавлено' + str(i))
        i = i + 1

