import telebot
import sqlite3
from config import TokenBot
from keybords import keybords
import topGame
import news
import json
import time
import habar
import muisk
import film
import addperformers

bot  = telebot.TeleBot(TokenBot)

listTextStart = ['Парсинг', 'Админ панель']
textListParsingMenu = ['Обычный', 'Премиум', 'Выйти']


class DataBased():
    def __init__(self):
        self.connect = sqlite3.connect('databased.db', check_same_thread=False)
        self.cursor = self.connect.cursor()
    
    def chek(self, piopleID):
        self.cursor.execute(f'SELECT userID FROM users WHERE userID = {piopleID}')
        return self.cursor.fetchone()

    def register(self, userID):
        self.cursor.execute(f'INSERT INTO users VALUES (?,?,?,0,0);', userID)
        self.connect.commit()

    def check_admin(self, piopleID):
        self.cursor.execute(f'SELECT admin FROM users WHERE userID = {piopleID}')
        return self.cursor.fetchone()

    def  add(self, messageText):
        self.cursor.execute(f' UPDATE users SET premium = 1 WHERE userID = {messageText}')
        self.connect.commit()

    def remove(self, messageText):
        self.cursor.execute(f'UPDATE users SET premium = 0 WHERE userID = {messageText}')
        self.connect.commit()

    def checkPremium(self, piopleID):
        self.cursor.execute(f'SELECT premium FROM users WHERE userID = {piopleID}')
        return self.cursor.fetchone()



@bot.message_handler(commands=['start'])
def start(message):
    piopleID = message.chat.id
    data = db.chek(piopleID)
    if data is None:
        userID = [piopleID, message.from_user.first_name, message.from_user.last_name]
        db.register(userID)
        bot.send_message(piopleID, f'Спасибо за регистрацыю {message.from_user.first_name} {message.from_user.last_name}', reply_markup=keybords(listTextStart))
    else:
        bot.send_message(piopleID, 'Поздравляю!! С тем что вы были за регестрированы', reply_markup=keybords(listTextStart))


@bot.message_handler(func=lambda m: m.text == 'Парсинг')
def parsing(message):
    bot.send_message(message.chat.id, 'Вберете котегорию', reply_markup=keybords(textListParsingMenu))


@bot.message_handler(func=lambda m: m.text == "Обычный")
def parsingPlain(message):
    text = ["Новости", 'Топ игр', 'Назат']
    bot.send_message(message.chat.id, 'Выберете котигорию для парсинга', reply_markup=keybords(text))

@bot.message_handler(func=lambda m: m.text == 'Премиум')
def parsingPeremium(message):
    piopleID = message.chat.id
    data = db.checkPremium(piopleID)
    if data[0] == 0:
        bot.send_message(piopleID, 'Прости но у тебя нет премиума')
    else:
        text = ['Хабар новости', 'Музыка', "Назат"]
        bot.send_message(piopleID, 'Выберете котигорию', reply_markup=keybords(text))

@bot.message_handler(func=lambda m: m.text == 'Админ панель')
def admin(message):
    piopleID = message.chat.id
    data = db.check_admin(piopleID)
    if data[0] == 1:
        text = ['Удалить премиум', 'Выдать премиум', 'Выйти', 'Обновить базу даных музыки']
        bot.send_message(piopleID, 'Здраствуйте админестратор', reply_markup=keybords(text))
    else:
        bot.send_message(piopleID, 'Прости мой друг но у тебя не хвотает прав')

@bot.message_handler(func=lambda m: m.text == 'Выйти')
def exit(message):
    bot.send_message(message.chat.id, 'Выхожу', reply_markup=keybords(listTextStart))


@bot.message_handler(func=lambda m: m.text == 'Назат')
def back(message):
    bot.send_message(message.chat.id, 'Возращяюсь назат', reply_markup=keybords(textListParsingMenu))

@bot.message_handler(func=lambda m: m.text == "Выдать премиум")
def addPremiumSent(message):
    data = db.check_admin(message.chat.id)
    if data[0] == 1:
        sent =  bot.reply_to(message, "Кому выдать премиум")
        bot.register_next_step_handler(sent, addPremium)


def addPremium(message):
    messageText = message.text
    data = db.chek(messageText)
    if data is None:
        bot.send_message(message.chat.id, f'Пользователя с ID {messageText} нет')
    else:
        db.add(messageText)
        bot.send_message(message.chat.id, f'Поздравляю с ID {messageText} был добавлен премиум')
        bot.send_message(messageText, "Вам выдан премиум пользуйтесь")



@bot.message_handler(func=lambda m: m.text == 'Удалить премиум')
def removePremiumSent(message):
    data = db.check_admin(message.chat.id)
    if data[0] == 1:
        sent = bot.reply_to(message, 'У кого удалить премиум')
        bot.register_next_step_handler(sent, removePremium)



def removePremium(message):
    messageText = message.text
    data = db.chek(messageText)
    if data is None:
        bot.send_message(message.chat.id, f'Пользователя с ID {messageText} нет')
    else:
        db.remove(messageText)
        bot.send_message(message.chat.id, f'У пользователя с ID {messageText} был удалён премиум')
        bot.send_message(messageText, 'Простите но у вас юыл удалён премиум. Я вам сочуствую')


@bot.message_handler(func=lambda m: m.text == 'Обновить базу даных музыки')
def updateDBMusik(message):
    data = db.check_admin(message.chat.id)
    if data[0] == 1:
        bot.send_message(message.chat.id, 'Обновляю базу даных')
        addperformers.addMusikDB()
        bot.send_message(message.chat.id, 'База даных обновлена')


@bot.message_handler(func=lambda m: m.text == 'Топ игр')
def topGameAnswer(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных...')
    topGame.topGame()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Статья: {item.get("article")}\nВыложена: {item.get("dataPost")}\nКол-во клментариев: {item.get("coments")}\nСылка: {item.get("link")}'
        
        if index % 20 == 0:
            time.sleep(5)

        bot.send_message(message.chat.id, card)
    
    bot.send_message(message.chat.id, 'Всё!!')

@bot.message_handler(func=lambda m: m.text == 'Новости')
def newAnsewr(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных....')

    news.newsParser()

    with open('parser.json',) as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Новость {item.get("article")}\nВыложкна: {item.get("dataPost")}\nСылка {item.get("links")}'

        if index % 20 == 0:
            time.sleep(5)

        bot.send_message(message.chat.id, card)

    bot.send_message(message.chat.id, 'Всё!!!')

@bot.message_handler(func=lambda m: m.text == 'Хабар новости')
def habrNews(message):
    date = db.checkPremium(message.chat.id)
    if date[0] == 1:
        sent = bot.reply_to(message, 'Сколько страниц')
        bot.register_next_step_handler(sent, habrNewsAnswer) 
    else:
        bot.send_message(message.chat.id, 'Так стоп, у тебя нет премиума но как ?')

def habrNewsAnswer(message):
    messageText = int(message.text)
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных....')
    habar.habrParser(messageText)

    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Статья: {item.get("article")}\nАвтор: {item.get("User")}\nДата выхода: {item.get("dataPost")}\nПросмотров: {item.get("views")}\nСылка: {item.get("links")}'

        if index % 20 == 0:
            time.sleep(5)

        bot.send_message(message.chat.id, card)
    bot.send_message(message.chat.id, 'Всё!!')

@bot.message_handler(func=lambda m: m.text == 'Топ фильмов')
def topFilm(message):
    date = db.checkPremium(message.chat.id)
    if date[0] == 1:
        sent = bot.reply_to(message, 'Сколько страниц')
        bot.register_next_step_handler(sent, topFilmAnswer)
    else:
        bot.send_message(message.chat.id, 'Так стоп у тебя нет премиума но как ?')


def topFilmAnswer(message):
    messageText = int(message.text)
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных')
    film.filmParser(messageText)

    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Фильм: {item.get("name")}\nМесто: {item.get("place")}\nЖанар: {item.get("genres")}\nОценка: {item.get("rating")}\nДата выхода и страна: {item.get("data")}\nСылка: {item.get("link")}'
        if index % 20 == 0:
            time.sleep(5)

        bot.send_message(message.chat.id, card)
    bot.send_message(message.chat.id, 'Всё!!!')

@bot.message_handler(func=lambda m: m.text == 'Музыка')
def musikAnswer(message):
    botMusikList = ['Популярныя музыка', 'Рок-н-ролл музыка', 'Новые треки', 'Джаз музыка', 'Рок музыка', 'Эстрада и ретро музыка', 'Электроника музыка', 'Артист', 'Назат']
    bot.send_message(message.chat.id, 'Выбери котигорию', reply_markup=keybords(botMusikList))


@bot.message_handler(func=lambda m: m.text == 'Популярныя музыка')
def pMusk(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных ...')
    muisk.popularMusk()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")

@bot.message_handler(func=lambda m: m.text == 'Рок-н-ролл музыка')
def rnrMusk(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных ...')
    muisk.rrMusic()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")

@bot.message_handler(func=lambda m: m.text == 'Новые треки')
def nMusk(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных ...')
    muisk.newMusik()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")

@bot.message_handler(func=lambda m: m.text == 'Джаз музыка')
def jMusk(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных ...')
    muisk.jazzMuski()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")



@bot.message_handler(func=lambda m: m.text == 'Рок музыка')
def rMusk(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных ...')
    muisk.rockMusik()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")


@bot.message_handler(func=lambda m: m.text == 'Эстрада и ретро музыка')
def eMusk(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных ...')
    muisk.erMusik()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")

@bot.message_handler(func=lambda m: m.text == 'Электроника музыка')
def electroMusk(message):
    bot.send_message(message.chat.id, 'Пожалуста подаждите идёт сбор даных ...')
    muisk.electronicsMusic()
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")

@bot.message_handler(func=lambda m: m.text == 'Артист')
def artist(message):
    sent = bot.reply_to(message, 'Имя исролнителя')
    bot.register_next_step_handler(sent, artistAnswer)


def artistAnswer(message):
    messageText = message.text
    bot.send_message(message.chat.id, 'подаждите идёт сбор даных')
    muisk.artist(messageText)
    with open('parser.json') as file:
        parser = json.load(file)

    for index, item in enumerate(parser):
        card = f'Название песни: {item.get("name")}\nАртист: {item.get("artist")}\nПродолжительность: {item.get("time")}\nСкачать: {item.get("link")}'
        bot.send_message(message.chat.id, card)
        if index % 20 == 0:
            time.sleep(5)
    bot.send_message(message.chat.id, "Всё!!!")

if __name__ == '__main__':
    db = DataBased()
    bot.polling()


