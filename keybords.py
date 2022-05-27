from telebot import types 

def keybords(keyList):
    kebord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kebord.add(*keyList)
    return kebord

