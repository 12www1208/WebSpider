from os import link
import requests
from bs4 import BeautifulSoup
import json
import sqlite3

def popularMusk():
    parser = []
    url = requests.get(f'https://ru.hitmotop.com/songs/top-today') 
    html = BeautifulSoup(url.text, "html.parser")

    blok = html.find_all('li', class_="tracks__item")

    for bloks in blok:
        name = (bloks.find('div', class_='track__title').text).replace(' ', '')
        artist = bloks.find('div', class_='track__desc').text
        time = bloks.find('div', class_='track__fulltime').text
        link = bloks.find('a', class_='track__download-btn').get('href')
        parser.append(
            {
                'name': name,
                'artist': artist,
                'time': time,
                'link': link
            }
        )
       
        with open('parser.json', 'w') as file:
            json.dump(parser, file, indent=4, ensure_ascii=False)


def newMusik():
    parser = []
    url = requests.get(f'https://ru.hitmotop.com/songs/new') 
    html = BeautifulSoup(url.text, "html.parser")

    blok = html.find_all('li', class_="tracks__item")

    for bloks in blok:
        name = (bloks.find('div', class_='track__title').text).replace(' ', '')
        artist = bloks.find('div', class_='track__desc').text
        time = bloks.find('div', class_='track__fulltime').text
        link = bloks.find('a', class_='track__download-btn').get('href')
        parser.append(
            {
                'name': name,
                'artist': artist,
                'time': time,
                'link': link
            }
        )
       
        with open('parser.json', 'w') as file:
            json.dump(parser, file, indent=4, ensure_ascii=False)



def jazzMuski():
    parser = []
    url = requests.get(f'https://ru.hitmotop.com/genre/39') 
    html = BeautifulSoup(url.text, "html.parser")

    blok = html.find_all('li', class_="tracks__item")

    for bloks in blok:
        name = (bloks.find('div', class_='track__title').text).replace(' ', '')
        artist = bloks.find('div', class_='track__desc').text
        time = bloks.find('div', class_='track__fulltime').text
        link = bloks.find('a', class_='track__download-btn').get('href')
        parser.append(
            {
                'name': name,
                'artist': artist,
                'time': time,
                'link': link
            }
        )
       
        with open('parser.json', 'w') as file:
            json.dump(parser, file, indent=4, ensure_ascii=False)



def rockMusik():
    parser = []
    url = requests.get(f'https://ru.hitmotop.com/genre/6') 
    html = BeautifulSoup(url.text, "html.parser")

    blok = html.find_all('li', class_="tracks__item")

    for bloks in blok:
        name = (bloks.find('div', class_='track__title').text).replace(' ', '')
        artist = bloks.find('div', class_='track__desc').text
        time = bloks.find('div', class_='track__fulltime').text
        link = bloks.find('a', class_='track__download-btn').get('href')
        parser.append(
            {
                'name': name,
                'artist': artist,
                'time': time,
                'link': link
            }
        )
       
        with open('parser.json', 'w') as file:
            json.dump(parser, file, indent=4, ensure_ascii=False)



def electronicsMusic():
    parser = []
    url = requests.get(f'https://ru.hitmotop.com/genre/8') 
    html = BeautifulSoup(url.text, "html.parser")

    blok = html.find_all('li', class_="tracks__item")

    for bloks in blok:
        name = (bloks.find('div', class_='track__title').text).replace(' ', '')
        artist = bloks.find('div', class_='track__desc').text
        time = bloks.find('div', class_='track__fulltime').text
        link = bloks.find('a', class_='track__download-btn').get('href')
        parser.append(
            {
                'name': name,
                'artist': artist,
                'time': time,
                'link': link
            }
        )
       
        with open('parser.json', 'w') as file:
            json.dump(parser, file, indent=4, ensure_ascii=False)


def erMusik():
    parser = []
    url = requests.get(f'https://ru.hitmotop.com/genre/5') 
    html = BeautifulSoup(url.text, "html.parser")

    blok = html.find_all('li', class_="tracks__item")

    for bloks in blok:
        name = (bloks.find('div', class_='track__title').text).replace(' ', '')
        artist = bloks.find('div', class_='track__desc').text
        time = bloks.find('div', class_='track__fulltime').text
        link = bloks.find('a', class_='track__download-btn').get('href')
        parser.append(
            {
                'name': name,
                'artist': artist,
                'time': time,
                'link': link
            }
        )
       
        with open('parser.json', 'w') as file:
            json.dump(parser, file, indent=4, ensure_ascii=False)


def rrMusic():
    parser = []
    url = requests.get(f'https://ru.hitmotop.com/genre/61') 
    html = BeautifulSoup(url.text, "html.parser")

    blok = html.find_all('li', class_="tracks__item")

    for bloks in blok:
        name = (bloks.find('div', class_='track__title').text).replace(' ', '')
        artist = bloks.find('div', class_='track__desc').text
        time = bloks.find('div', class_='track__fulltime').text
        link = bloks.find('a', class_='track__download-btn').get('href')
        parser.append(
            {
                'name': name,
                'artist': artist,
                'time': time,
                'link': link
            }
        )
       
        with open('parser.json', 'w') as file:
            json.dump(parser, file, indent=4, ensure_ascii=False)



def artist(a):
    x = 0
    lnkList = []
    parser = []
    connect = sqlite3.connect('databased.db', check_same_thread=False)
    cursor = connect.cursor()

    for name in cursor.execute('SELECT link FROM performers WHERE name LIKE ?', ('%'+a+'%',)):
        lnkList.append(name[0])
        
        for link in lnkList:
            while True:
                x += 48
                url = requests.get(f'{link}/start/{x}')
                html = BeautifulSoup(url.text, 'html.parser')
                blok = html.find_all('li', class_='tracks__item')
            
                for bloks in blok:
                    name = (bloks.find('div', class_='track__title').text).replace(' ', '')
                    artist = bloks.find('div', class_='track__desc').text
                    time = bloks.find('div', class_='track__fulltime').text
                    links = bloks.find('a', class_='track__download-btn').get('href')
                    parser.append(
                        {
                            'name': name,
                            'artist': artist,
                            'time': time,
                            'link': links
                        }
                    )
                if x == 432:
                    break
       
    with open('parser.json', 'w') as file:
        json.dump(parser, file, indent=4, ensure_ascii=False)





