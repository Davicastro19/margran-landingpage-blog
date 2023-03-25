# markups.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('⬅ Main Menu')
btnOtherMain = KeyboardButton('⬅ Back')
btnFoodMain = KeyboardButton('⬅ Back')

# Main Menu :
btnLogin = KeyboardButton('👤')
btnConfTo = KeyboardButton('⚙️')
btnConfOne = KeyboardButton('🛠')
btnExitDes = KeyboardButton('📴 Sair e Desconectar')
btnGo = KeyboardButton('▶️')
btnStop = KeyboardButton('⏸')
btnSave = KeyboardButton('🗂')
btnReset = KeyboardButton('♻️')
btnInform = KeyboardButton('📑')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnLogin, btnConfTo, btnConfOne,btnGo,btnStop,btnInform,btnReset,btnSave)


# Sub Other Menu:
subOtherMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnOtherMain)

# Food Menu:
subFoodMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFoodMain)



btnstrategy = KeyboardButton('🔩 Estratégia')
btngale = KeyboardButton('🔩 Gale')
btnfactorGale = KeyboardButton('🔩 Fator do Gale')
btnnivel = KeyboardButton('🔩 Nivel')
btnpreStop = KeyboardButton('🔩 Pré Stop')
btndoji = KeyboardButton('🔩 Pós Doji')
btninvest = KeyboardButton('🔩 Entrada')
btnstopWin = KeyboardButton('🔩 Stop Win')
btnstopLoss = KeyboardButton('🔩 Stop Loss')
btntypeSignals = KeyboardButton('🔩 Tipo de Sala')
btnsignals = KeyboardButton('🔩 Sinais')
btndate = KeyboardButton('🔩 Data')
btntouros = KeyboardButton('🔩 Touros')
btnmaxSim = KeyboardButton('🔩 Max. Simutâneas')
btntypeEnter = KeyboardButton('🔩 Tipo de Entrada')
btnfactorCiclos = KeyboardButton('🔩 Fator do ciclos')
btntrend = KeyboardButton('🔩 Tendência')
btnpay = KeyboardButton('🔩 PayOut')
btndelay = KeyboardButton('🔩 Delay')
btnMain = KeyboardButton('🌐')


mainconfig = ReplyKeyboardMarkup(resize_keyboard = True)
mainconfig.add(btnMain)
mainconfig.add(btnfactorCiclos)
mainconfig.add(btntrend)
mainconfig.add(btndelay)
mainconfig.add(btnstrategy)
mainconfig.add(btngale)
mainconfig.add(btnfactorGale)
mainconfig.add(btnnivel)
mainconfig.add(btnpreStop)
mainconfig.add(btndoji)
mainconfig.add(btninvest)
mainconfig.add(btnstopWin)
mainconfig.add(btnstopLoss)
mainconfig.add(btntypeSignals)
mainconfig.add(btnsignals)
mainconfig.add(btndate)
mainconfig.add(btntouros)
mainconfig.add(btnmaxSim)
mainconfig.add(btntypeEnter)
mainconfig.add(btnpay)



