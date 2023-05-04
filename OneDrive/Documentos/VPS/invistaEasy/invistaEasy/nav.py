# markups.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btntrd = KeyboardButton('📊TENDÊNCIA📊')
btnchk = KeyboardButton('📝CHECK LIST📝')
#btnest = KeyboardButton('💹CATALOGAR ESTRATÉGIA💹')
btnntc = KeyboardButton('📡NOTÍCIAS📡')
btnsinn = KeyboardButton('🔰CATALOGAR SINAIS🔰')
btnsinnii = KeyboardButton('🔰CATALOGAR SINAIS II🔰')
btncalc = KeyboardButton('🔢CALCULADORAS🔢')
btnjursc = KeyboardButton('🔣JUROS COMPOSTO🔣')
a = [ btnsinn,btnsinnii,btnchk, btnjursc,btntrd,btncalc,btnntc]

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
for i in a:
    mainMenu.add(i)


