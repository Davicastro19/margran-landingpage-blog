from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_polling 
from Controller.controlDao import connectDao
from Controller.controlEnum import MENSAGE
from aiogram.types import ParseMode
from Controller.validation import validate
from Controller.datesTimes import date
from Controller.fileSettings import file
from Controller.message import controlMessage
from multiprocessing import Process
from cryptography.fernet import Fernet
from Controller.main import comand
import nav,os,signal,logging, time, threading

logging.basicConfig(level=logging.INFO)
#1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0
API_TOKEN = '6211086543:AAFr0Ed1wFNEvLUxV2g48KSOzKYS2n9Ejr8' #
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def hello_throttled(*args, **kwargs):
    message = args[0]
    await message.answer("O tempo é de 2s - Aguarde.")

	
class Formsig(StatesGroup):
	email = State()
	senha = State()
	token = State()
	finish = State()


@dp.message_handler(commands='ativar')
async def cmstart(message: types.Message):
	await Formsig.email.set()
	await message.reply("Oi {0}, Qual código de compra?\n\n(Foi enviado em seu email)".format(message.chat.first_name))

@dp.message_handler(commands=['id'])
@dp.throttled(hello_throttled, rate=0)
async def command_stsssart(message: types.Message):
	await message.reply(str(message.chat.id))

@dp.message_handler(commands=['cr'])
@dp.throttled(hello_throttled, rate=0)
async def command_stsssart(message: types.Message):
	try:
		namfile = message.text.split(' ')[1]
		file.create(str(namfile))
	except Exception as a:
		controlMessage.send_msg("Faha ao criar arquivo", '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')

@dp.message_handler(commands=['start'])
@dp.throttled(hello_throttled, rate=0)
async def command_start(message: types.Message):
	if os.path.exists(str(message.chat.id)+'.txt') == False:
		#check, config =  connectDao.selectConfigById(str(message.chat.id))
		if True:
		#	file.restoreData(str(message.chat.id),config)
		#	await bot.send_message(message.from_user.id, f'Oi {message.from_user.first_name}, vamos começar?', reply_markup = nav.mainMenu)
	
		#else:
			await bot.send_message(message.chat.id,MENSAGE.ALL.value.format(message.chat.first_name,message.chat.id),parse_mode=ParseMode.HTML)
			await bot.send_message(message.chat.id,MENSAGE.MSG005.value,parse_mode=ParseMode.HTML)
			file.create(str(message.chat.id))
	else:
		await bot.send_message(message.from_user.id, f'Oi {message.from_user.first_name}, vamos começar?', reply_markup = nav.mainMenu)
class sendmsg(StatesGroup):
	msg = State()
	finish = State()
class Formto(StatesGroup):
	cods = State()
class FormGo(StatesGroup):
	cods = State()
class FormConfig(StatesGroup):
	typeStrategy = State()
	gale = State()
	nivel = State()
	factorGale = State()
	factorCiclos = State()
	preStop = State()
	doji = State()
	touros = State()
	trend = State()
	maxSim = State()
	typeEnter = State()
	invest = State()
	stopWin = State()
	stopLoss = State()
	typeSignals = State()
	signals = State()
	pay = State()
	date = State()
	finish = State()


@dp.message_handler(commands='config')
@dp.throttled(hello_throttled, rate=0)
async def cmd_strategy(message: types.Message):
	await FormConfig.typeStrategy.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("SorosGale", "Gale","Ciclos","Fixa","Cancelar")
	await message.reply("Qual tipo de gerenciamento para recuperação estou habilitado a usar hoje?",reply_markup=markup)



@dp.message_handler(lambda message: message.text not in ["SorosGale", "Gale","Ciclos","Fixa","Cancelar"], state=FormConfig.typeStrategy)
@dp.throttled(hello_throttled, rate=0)
async def process_typeStrategy_invalid(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("SorosGale", "Gale","Ciclos","Fixa","Cancelar")
    return await message.reply("Estrategia Errada, escolha a opção no teclado: 'SorosGale', 'Gale','Ciclos','Fixa','Cancelar'", reply_markup=markup)


@dp.message_handler(state=FormConfig.typeStrategy)
@dp.throttled(hello_throttled, rate=0)
async def process_typeStrategy(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['typeStrategy'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("Cancelado", reply_markup=nav.mainMenu)
		await state.finish()
	elif data['typeStrategy'] != 'Fixa':
		await FormConfig.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("0","1","2","3","4","5","Cancelar")
		await message.reply("Quantos gales?",reply_markup=markup)
	else:
		await FormConfig.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","Cancelar")
		await message.reply("Confirmar?",reply_markup=markup)
	#
#
@dp.message_handler(lambda message: message.text not in ["0","1","2","3","4","5","Cancelar","SIM"], state=FormConfig.gale)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale_invalid(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("0","1","2","3","4","5","Cancelar")
	return await message.reply('Quantos gales? escolha a opção no teclado: "0","1","2","3","4","5","Cancelar" ',reply_markup=markup)

@dp.message_handler(state=FormConfig.gale)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		if message.text ==  'SIM':
			data['gale'] ='0'
		else:
			data['gale'] =message.text
	if "Cancelar" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	elif data['typeStrategy'] in ["Gale","Fixa"] :
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		await FormConfig.next()
		markup.add("SIM","NÃO")
		await message.reply("Posso prosseguir?",reply_markup=markup)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","2","3","4")
		markup.add("5","6","7","8")
		await FormConfig.next()
		await message.reply("Quantos niveis?",reply_markup=markup)

	
	
@dp.message_handler(lambda message: message.text not in ["0","1","2", "3", "4","5", "6", "7", "8",'NÃO','SIM'], state=FormConfig.nivel)
@dp.throttled(hello_throttled, rate=0)
async def process_typenivel_invalid(message: types.Message):
	return await message.reply('Quantos Niveis? escolha a opção no teclado: "0","1","2", "3", "4","5", "6", "7", "8","NÃO","SIM"')

@dp.message_handler(state=FormConfig.nivel)
@dp.throttled(hello_throttled, rate=0)
async def process_typeNivel(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		if message.text ==  'SIM':
			data['nivel'] = 0
		else:
			data['nivel'] = message.text
	if data['typeStrategy'] in ["SorosGale","Fixa"]:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("0")
		await FormConfig.next()
		await message.reply("Qual fator de multiplicação do gale?",reply_markup=markup)
	elif "NÃO" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1.1","1.2","1.3")
		markup.add("1.4","1.5","1.6")
		markup.add("1.7","1.8","1.9","2.0")
		markup.add("2.1","2.2","2.3")
		markup.add("2.4","2.5","2.6")
		markup.add("2.7","2.8","2.9","Cancelar")
		await FormConfig.next()
		await message.reply("Qual fator de multiplicação do gale?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.0","2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9","Cancelar"], state=FormConfig.factorGale)
@dp.throttled(hello_throttled, rate=0)
async def process_typeFActorgale_invalid(message: types.Message):
	return await message.reply("Qual fator de multiplicação do gale? escolha a opção no teclado")


@dp.message_handler(state=FormConfig.factorGale)
async def process_factorGale(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['factorGale'] = message.text
	if data['typeStrategy'] in ["Gale","SorosGale","Fixa"]:
		await FormConfig.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO")
		await message.reply("Posso prosseguir?",reply_markup=markup)
	elif "Cancelar" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1.1","1.2","1.3")
		markup.add("1.4","1.5","1.6")
		markup.add("1.7","1.8","1.9")
		markup.add("2.1","2.2","2.3")
		markup.add("2.4","2.5","2.6")
		markup.add("2.7","2.8","2.9","Cancelar")
		await FormConfig.next()
		await message.reply("Qual fator do ciclos?",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["NÃO","SIM","0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9","Cancelar","SIM"], state=FormConfig.factorCiclos)
@dp.throttled(hello_throttled, rate=0)
async def process_typefactorCis_invalid(message: types.Message):
	return await message.reply("Qual fator do ciclos? escolha a opção no teclado")


@dp.message_handler(state=FormConfig.factorCiclos)
@dp.throttled(hello_throttled, rate=0)
async def process_factorCiclos(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		if message.text ==  'SIM':
			data['factorCiclos'] = '0'
		else:
			data['factorCiclos'] = message.text
	if "Cancelar" in message.text or "NÃO" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("ON","OFF","Cancelar")
		await FormConfig.next()
		await message.reply("Ativar Pré Stop?",reply_markup=markup)



@dp.message_handler(lambda message: message.text not in ["ON","OFF","Cancelar"], state=FormConfig.preStop)
@dp.throttled(hello_throttled, rate=0)
async def process_typepreStop_invalid(message: types.Message):
	return await message.reply("Ativar Pré Stop? escolha a opção no teclado")


@dp.message_handler(state=FormConfig.preStop)
@dp.throttled(hello_throttled, rate=0)
async def process_preStop(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['preStop'] = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("ON","OFF","Cancelar")
	if "Cancelar" in message.text or "NÃO" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	else:
		await FormConfig.next()
		await message.reply("Ativar Pós-Doji?  (Ativando esta opção não pararei de operar o sinal após o doji)",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["ON","OFF","Cancelar"], state=FormConfig.doji)
@dp.throttled(hello_throttled, rate=0)
async def process_typedoji_invalid(message: types.Message):
	return await message.reply("Ativar Pós-Doji?  escolha a opção no teclado")

@dp.message_handler(state=FormConfig.doji)
@dp.throttled(hello_throttled, rate=0)
async def process_doji(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['doji'] = message.text
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("0","1","2","3","Cancelar")
	if "Cancelar" in message.text:
		await state.finish()
	else:
		await FormConfig.next()
		await message.reply("Permitir até quantos touros?(0 - Desativado)",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["0","1","2","3","Cancelar"], state=FormConfig.touros)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Permitir até quantos touros? escolha a opção no teclado")

@dp.message_handler(state=FormConfig.touros)
@dp.throttled(hello_throttled, rate=0)
async def procesypeGale(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['touros'] =message.text
	if "Cancelar" in message.text:
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("ON","OFF",'cancelar')
		await FormConfig.next()
		await message.reply("Ativar análise de tendência?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["ON","OFF","Cancelar"], state=FormConfig.trend)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Ativar análise de tendência? escolha a opção no teclado")

@dp.message_handler(state=FormConfig.trend)
@dp.throttled(hello_throttled, rate=0)
async def procesypeGale(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['trend'] =message.text
	if "Cancelar" in message.text:
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","2","3","4","5","Cancelar")
		await FormConfig.next()
		await message.reply("Maxímo de entradas simutanêas?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["1","2","3","4","5","Cancelar"], state=FormConfig.maxSim)
@dp.throttled(hello_throttled, rate=0)
async def process_type_invalid(message: types.Message):
	return await message.reply("Maxímo de entradas simutanêas? escolha a opção no teclado")

@dp.message_handler(state=FormConfig.maxSim)
@dp.throttled(hello_throttled, rate=0)
async def process_typele(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['maxSim'] =message.text
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("Valores","Porcentagem",'Cancelar')
		if "Cancelar" in message.text or "NÃO" in message.text:
			await message.reply("Cancelado > /start",reply_markup=markup)
			await state.finish()
		else:
			await FormConfig.next()
			await message.reply("Qual tipo de entrada usaremos?",reply_markup=markup)
	

@dp.message_handler(lambda message: message.text not in ["Valores","Porcentagem",'Cancelar'], state=FormConfig.preStop)
@dp.throttled(hello_throttled, rate=0)
async def process_typepreStop_invalid(message: types.Message):
	return await message.reply("Qual tipo de entrada usaremos? escolha a opção no teclado")


@dp.message_handler(state=FormConfig.typeEnter)
@dp.throttled(hello_throttled, rate=0)
async def process_preStop(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['typeEnter'] = message.text
		if "Valores" in  data['typeEnter']:
			data['typeEnter'] = "R$"
		elif "Porcentagem" in  data['typeEnter']:
			data['typeEnter'] = "%"
		else:
			data['typeEnter'] = "%"

	if "Cancelar" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	elif "%" in data['typeEnter']:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","2","3","4","5","6","7","8","9",
		"10","11","12","13","14","15","16","17","18","19",
		"20","21","22","23","24","25","26","27","28","29",
		"30","31","32","33","34","35","36","37","38","39",
		"40","41","42","43","44","45","46","47","48","49",
		"50","51","52","53","54","55","56","57","58","59",
		"60","61","62","63","64","65","66","67","68","69",
		"70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99")
		await FormConfig.next()
		await message.reply("Quantos porcentegem de entrada?",reply_markup=markup)
	else:
		await FormConfig.next()
		await message.reply("Qual o valor da entrada?",reply_markup=markup)

@dp.message_handler(lambda message: message.text != validate.is_number(message.text.replace(",",".")), state=FormConfig.invest)
@dp.throttled(hello_throttled, rate=0)
async def process_typeinvest_invalid(message: types.Message):
	return await message.reply("Quantidade invalida, digite um valor flutuante  - Ex: 'R$2', '$2' ou '2%' deve ser colocado assim: 2.00\nou\n'EX:R$3,30', '$3,30' ou '2,30%' deve ser colocado assim 3.30 :\nou\n'EX:R$100,00', '$100,00' ou '100,00%' deve ser colocado assim 100.00 :\n")

@dp.message_handler(state=FormConfig.invest)
@dp.throttled(hello_throttled, rate=0)
async def process_invest(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['invest'] = message.text
	if data['typeEnter'] == "%":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","2","3","4","5","6","7","8","9",
		"10","11","12","13","14","15","16","17","18","19",
		"20","21","22","23","24","25","26","27","28","29",
		"30","31","32","33","34","35","36","37","38","39",
		"40","41","42","43","44","45","46","47","48","49",
		"50","51","52","53","54","55","56","57","58","59",
		"60","61","62","63","64","65","66","67","68","69",
		"70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99")
		await FormConfig.next()
		await message.reply("Qual é a meta de Stop Win?(%)",reply_markup=markup)
	else:
		await FormConfig.next()
		await message.reply("Qual é a meta de Stop Win?(R$)",reply_markup=markup)

	


@dp.message_handler(lambda message: message.text != validate.is_param(message.text), state=FormConfig.stopWin)
@dp.throttled(hello_throttled, rate=0)
async def process_typestopWin_invalid(message: types.Message):
	return await message.reply("Qual é a meta de Stop Win?(R$) escolha a opção no teclado")


@dp.message_handler(state=FormConfig.stopWin)
@dp.throttled(hello_throttled, rate=0)
async def process_stopWin(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		if message.text ==  'SIM':
			data['stopWin'] = '0'
		else:
			data['stopWin'] = message.text
	if data['typeEnter'] == "%":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","2","3","4","5","6","7","8","9",
		"10","11","12","13","14","15","16","17","18","19",
		"20","21","22","23","24","25","26","27","28","29",
		"30","31","32","33","34","35","36","37","38","39",
		"40","41","42","43","44","45","46","47","48","49",
		"50","51","52","53","54","55","56","57","58","59",
		"60","61","62","63","64","65","66","67","68","69",
		"70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99")
		await FormConfig.next()
		await message.reply("Qual o valor do Stop Loss?(%)",reply_markup=markup)
	elif "NÃO" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
			
	else:
		await FormConfig.next()
		await message.reply("Qual o valor do Stop Loss?(R$)",reply_markup=markup)



@dp.message_handler(lambda message: message.text != validate.is_param(message.text), state=FormConfig.stopLoss)
@dp.throttled(hello_throttled, rate=0)
async def process_typestopLoss_invalid(message: types.Message):
	return await message.reply("Qual o valor do Stop Loss? escolha a opção no teclado")

@dp.message_handler(state=FormConfig.stopLoss)
@dp.throttled(hello_throttled, rate=0)
async def process_stopLoss(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		if message.text ==  'SIM':
			data['stopLoss'] = '0'
		else:
			data['stopLoss'] = message.text
	if "Cancelar" in message.text or "NÃO" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	else:
		await FormConfig.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("Meus Sinais","Cancelar")
		await message.reply("Qual lista de ordens pretende utilizar?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["Meus Sinais","ALLWINSIGNALS","Cancelar"], state=FormConfig.typeSignals)
@dp.throttled(hello_throttled, rate=0)
async def process_typesig_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido - "Meus Sinais ou ALLWINSIGNALS"',parse_mode=ParseMode.HTML)
	

@dp.message_handler(state=FormConfig.typeSignals)
@dp.throttled(hello_throttled, rate=0)
async def process_typeSignalsnals(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['typeSignals'] = message.text
	if "Cancelar" in message.text or "NÃO" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	elif data['typeSignals'] == 'Meus Sinais':
		await FormConfig.next()
		await message.reply('''Me envie a sua lista de ordens! - Formato:\n
	A lista não pode conter espaços no final: 
	\n
	M5;EURGBP-OTC;12:35:00;PUT
	M5;USDJPY-OTC;13:10:00;PUT
	M5;EURGBP-OTC;13:15:00;PUT
	M5;EURJPY-OTC;13:15:00;PUT
	\n
	após cada sinal, pular a linha sem espaço.''',reply_markup=markup)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("LISTA")
		await message.reply("ALLWINSIGNALS - ESCOLHA UMA SALA.",reply_markup=markup)
		await FormConfig.next()


@dp.message_handler(lambda message: True != validate.listSigns(message.text) and message.text not in ["LISTA","OTC","M1","M5-24h","M15-24h","M30-24h","H1-24h"], state=FormConfig.signals)
@dp.throttled(hello_throttled, rate=0)
async def process_typed_invalid(message: types.Message):
	check, lista, reason = validate.datailsListSigns(message.text)
	if check == False:
		return await message.reply(reason)
	else:
		return await message.reply('há um erro')
	

@dp.message_handler(state=FormConfig.signals)
@dp.throttled(hello_throttled, rate=0)
async def process_signals(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['signals'] = message.text
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("0","1")
		await FormConfig.next()
		await message.reply("Qual payout deseja usar?\n0 - Binaria\n1 - Digital",reply_markup=markup)



@dp.message_handler(lambda message: message.text != validate.is_param(message.text), state=FormConfig.pay)
@dp.throttled(hello_throttled, rate=0)
async def process_typestopLoss_invalid(message: types.Message):
	return await message.reply("Qual o valor do Payout? escolha a opção no teclado")

@dp.message_handler(state=FormConfig.pay)
@dp.throttled(hello_throttled, rate=0)
async def process_stopLoss(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['pay'] = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add(date.currentDateString(),date.dateTomorrowString(),"Cancelar")
	await FormConfig.next()
	await message.reply("Em qual data irei rodar estas ordens?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in [date.currentDateString(),date.dateTomorrowString(),"Cancelar"], state=FormConfig.date)
@dp.throttled(hello_throttled, rate=0)
async def process_typedate_invalid(message: types.Message):
	return await message.reply("Em qual data irei rodar estas ordens? escolha a opção no teclado")
	
@dp.message_handler(state=FormConfig.date)
@dp.throttled(hello_throttled, rate=0)
async def process_optionsdate(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	if "Cancelar" in message.text or "NÃO" in message.text:
		await message.reply("Cancelado > /start",reply_markup=markup)
		await state.finish()
	else:
		async with state.proxy() as data:
			data['date'] = message.text
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO")
		await FormConfig.next()
		await message.reply("Vamos para a batalha?",reply_markup=markup)

@dp.message_handler(state=FormConfig.finish)
@dp.throttled(hello_throttled, rate=0)
async def process_FINSH(message: types.Message, state: FSMContext):
	global API_TOKEN
	async with state.proxy() as data:
		try:
			data['finish'] = message.text
			if data['finish'] == "SIM":
				file.alterParameter(str(message.chat.id),'touros',data['touros'])
				file.alterParameter(str(message.chat.id),'maxSim',data['maxSim'])
				file.alterParameter(str(message.chat.id),'typeStrategy',data['typeStrategy'])
				file.alterParameter(str(message.chat.id),'factorCiclos',data['factorCiclos'])
				file.alterParameter(str(message.chat.id),'factorGale',data['factorGale'])
				file.alterParameter(str(message.chat.id),'nivel',data['nivel'])
				file.alterParameter(str(message.chat.id),'preStop',data['preStop'])
				file.alterParameter(str(message.chat.id),'signals',data['signals'])
				file.alterParameter(str(message.chat.id),'typeEnter',data['typeEnter'])
				file.alterParameter(str(message.chat.id),'doji',data['doji'])
				file.alterParameter(str(message.chat.id),'gale',data['gale'])
				file.alterParameter(str(message.chat.id),'trend',data['trend'])
				file.alterParameter(str(message.chat.id),'invest',data['invest'])
				file.alterParameter(str(message.chat.id),'stopWin',data['stopWin'])
				file.alterParameter(str(message.chat.id),'stopLoss',data['stopLoss'])
				file.alterParameter(str(message.chat.id),'typeSignals',data['typeSignals'])
				file.alterParameter(str(message.chat.id),'date',data['date'])
				file.alterParameter(str(message.chat.id),'pay',data['pay'])
				file.alterParameter(str(message.chat.id),'delay','5')
				await message.reply("Ok {0}, salvo. ▶️".format(message.chat.first_name),reply_markup=nav.mainMenu)
				await state.finish()
			else:
				await message.reply("Ok {0} cancelado".format(message.chat.first_name),reply_markup=nav.mainMenu)
		except Exception as a:
			if 'FileNotFoundError' in str(a) or 'No such file or directory' in str(a):
				await message.reply("Oi {0}, faça primeiro Login ".format(message.chat.first_name),reply_markup=nav.mainMenu)
				await state.finish()
			else:
				await message.reply("{0},ERRO FormConfig.finish "+str(a).format(message.chat.first_name),reply_markup=nav.mainMenu)
				await state.finish()
	await state.finish()


class FormFPayout(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_fcpayou')
@dp.throttled(hello_throttled, rate=0)
async def cmd_fcpayou(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("0","1")
	await FormFPayout.value.set()
	await message.reply("Qual payout deseja usar?\n0 - Binaria\n1 - Digital",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99"], state=FormFPayout.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typevalue_invalid(message: types.Message):
	return await message.reply("Qual valor do payout? escolha a opção no teclado")

@dp.message_handler(state=FormFPayout.value)
@dp.throttled(hello_throttled, rate=0)
async def process_empayl(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] = message.text
			file.alterParameter(str(message.chat.id),'pay',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL- state=FormFPayout.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
class FormTyeNTER(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_stpretypeEnter')
@dp.throttled(hello_throttled, rate=0)
async def cmd_stpretypeEnter(message: types.Message): 
	await FormTyeNTER.value.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("%","R$")
	await message.reply("Qual tipo de investimento?",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["%","R$"], state=FormTyeNTER.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typepreStop_invalid(message: types.Message):
	return await message.reply("Qual tipo de investimento? escolha a opção no teclado")

@dp.message_handler(state=FormTyeNTER.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeNivel(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'typeEnter',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)
		controlMessage.send_msg("BOTALLWINTELL-  FormTyeNTER.value"+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormMmax(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_Mmax')
@dp.throttled(hello_throttled, rate=0)
async def cmd_Mmax(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("1","2","3")
	await FormMmax.value.set()
	await message.reply("Maxímo de entradas simutanêas?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["1","2","3"], state=FormMmax.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Maxímo de entradas simutanêas? escolha a opção no teclado")

@dp.message_handler(state=FormMmax.value)
async def process_typeinvess(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'maxSim',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)	
		controlMessage.send_msg("BOTALLWINTELL-  =FormMmax.value"+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
class FormTTouros(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_sTouros')
@dp.throttled(hello_throttled, rate=0)
async def cmd_sTouros(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("0","1","2","3")
	await FormTTouros.value.set()
	await message.reply("Permitir até quantos touros?(0 - Desativado)",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["0","1","2","3"], state=FormTTouros.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Permitir até quantos touros? escolha a opção no teclado")

@dp.message_handler(state=FormTTouros.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeinvess(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'touros',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL- FormTTouros.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')

		pass



class FormTyDatess(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_sdataess')
@dp.throttled(hello_throttled, rate=0)
async def cmd_sdataess(message: types.Message):
	await FormTyDatess.value.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add(date.currentDateString(),date.dateTomorrowString())
	await message.reply("Em qual data irei rodar estas ordens?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in [date.currentDateString(),date.dateTomorrowString()], state=FormTyDatess.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typedate_invalid(message: types.Message):
	return await message.reply("Data: escolha a opção no teclado")


@dp.message_handler(state=FormTyDatess.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typestopLosss(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'date',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)	
		controlMessage.send_msg("BOTALLWINTELL-FormTyDatess.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormTySignals(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_stypeSignals')
@dp.throttled(hello_throttled, rate=0)
async def cmd_stypeSignals(message: types.Message):
	await FormTySignals.value.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("Meus Sinais")
	await message.reply("Qual lista de ordens pretende utilizar?",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Meus Sinais","ALLWINSIGNALS"], state=FormTySignals.value)
async def process_typesig_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido - "Meus Sinais ou ALLWINSIGNALS"',parse_mode=ParseMode.HTML)
	

@dp.message_handler(state=FormTySignals.value)
async def process_typestopLosss(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'typeSignals',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)
		controlMessage.send_msg("BOTALLWINTELL-FormTySignals.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')		
		pass

class FormTstopLoss(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_sstopWin')
@dp.throttled(hello_throttled, rate=0)
async def cmd_sstopLoss(message: types.Message):
	try:
		conf  = file.get(message.chat.id)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		if conf['typeEnter'] == "%":
			markup.add("1","2","3","4","5","6","7","8","9",
			"10","11","12","13","14","15","16","17","18","19",
			"20","21","22","23","24","25","26","27","28","29",
			"30","31","32","33","34","35","36","37","38","39",
			"40","41","42","43","44","45","46","47","48","49",
			"50","51","52","53","54","55","56","57","58","59",
			"60","61","62","63","64","65","66","67","68","69",
			"70","71","72","73","74","75","76","77","78","79",
			"80","81","82","83","84","85","86","87","88","89",
			"90","91","92","93","94","95","96","97","98","99")
			await FormTstopLoss.value.set()
			await message.reply("Qual é a meta de Stop Loss?(%)",reply_markup=markup)
		else:
			await FormTstopLoss.value.set()
			await message.reply("Qual é a meta de Stop Loss?(R$)",reply_markup=markup)
	except Exception as a:
		if 'No such file or directory' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando /start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg(" ERRO  828 "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
	


@dp.message_handler(lambda message: message.text !=validate.is_param(message.text), state=FormTstopLoss.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typesstopLoss(message: types.Message):
	return await message.reply("Qual é a meta de Stop Loss? escolha a opção no teclado")


@dp.message_handler(state=FormTstopLoss.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typestopLosss(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'stopLoss',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  FormTstopLoss.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormTstopWin(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_sstopWin')
@dp.throttled(hello_throttled, rate=0)
async def cmd_sstopWin(message: types.Message):
	try:
		conf  = file.get(message.chat.id)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		if conf['typeEnter'] == "%":
			markup.add("1","2","3","4","5","6","7","8","9",
			"10","11","12","13","14","15","16","17","18","19",
			"20","21","22","23","24","25","26","27","28","29",
			"30","31","32","33","34","35","36","37","38","39",
			"40","41","42","43","44","45","46","47","48","49",
			"50","51","52","53","54","55","56","57","58","59",
			"60","61","62","63","64","65","66","67","68","69",
			"70","71","72","73","74","75","76","77","78","79",
			"80","81","82","83","84","85","86","87","88","89",
			"90","91","92","93","94","95","96","97","98","99")
			await FormTstopWin.value.set()
			await message.reply("Qual é a meta de Stop Win?(%)",reply_markup=markup)
		else:
			await FormTstopWin.value.set()
			await message.reply("Qual é a meta de Stop Win?(R$)",reply_markup=markup)
	except Exception as a:
		if 'No such file or directory' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg(" ERRO  882 "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

	


@dp.message_handler(lambda message: message.text !=validate.is_number(message.text), state=FormTstopWin.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typesstopWin(message: types.Message):
	return await message.reply("Qual é a meta de Stop Win? escolha a opção no teclado")



@dp.message_handler(state=FormTstopWin.value)
async def process_typestopWins(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'stopWin',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  ormTstopWin.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormTinves(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_sinves')
async def cmd_sinves(message: types.Message):
	try:
		conf  = file.get(message.chat.id)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		if conf['typeEnter'] == "%":
			markup.add("1","2","3","4","5","6","7","8","9",
			"10","11","12","13","14","15","16","17","18","19",
			"20","21","22","23","24","25","26","27","28","29",
			"30","31","32","33","34","35","36","37","38","39",
			"40","41","42","43","44","45","46","47","48","49",
			"50","51","52","53","54","55","56","57","58","59",
			"60","61","62","63","64","65","66","67","68","69",
			"70","71","72","73","74","75","76","77","78","79",
			"80","81","82","83","84","85","86","87","88","89",
			"90","91","92","93","94","95","96","97","98","99")
			await FormTinves.value.set()
			await message.reply("Qual a entrada?(%)",reply_markup=markup)
		else:
			await FormTinves.value.set()
			await message.reply("Qual a entrada?(R$)",reply_markup=markup)
	except Exception as a:
		if 'No such file or directory' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg(" ERRO  936 "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

	


@dp.message_handler(lambda message: message.text != validate.is_param(message.text), state=FormTinves.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typesinves(message: types.Message):
	return await message.reply("Qual é o investimento? escolha a opção no teclado")



@dp.message_handler(state=FormTinves.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeinvess(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'invest',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  FormTinves.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormTPdoji(StatesGroup):
	value = State()

@dp.message_handler(commands='cmd_stpredoji')
@dp.throttled(hello_throttled, rate=0)
async def cmd_stpredoji(message: types.Message):
	await FormTPdoji.value.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("ON","OFF")
	await message.reply("Ativar Pós Doji?",reply_markup=markup)



@dp.message_handler(lambda message: message.text not in ["ON","OFF"], state=FormTPdoji.value)
async def process_typepreStop_invalid(message: types.Message):
	return await message.reply("Ativar Pós Doji? escolha a opção no teclado")

@dp.message_handler(state=FormTPdoji.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeNivel(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'doji',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  FormTPdoji.value) "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
class FormTPstop(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_stprestop')
@dp.throttled(hello_throttled, rate=0)
async def cmd_stprestop(message: types.Message):
	await FormTPstop.value.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("ON","OFF")
	await message.reply("Ativar Pré Stop?",reply_markup=markup)



@dp.message_handler(lambda message: message.text not in ["ON","OFF"], state=FormTPstop.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typepreStop_invalid(message: types.Message):
	return await message.reply("Ativar Pré Stop? escolha a opção no teclado")

@dp.message_handler(state=FormTPstop.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeNivel(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'preStop',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  FormTPstop.value) "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
class FormTNivel(StatesGroup):
	value = State()

@dp.message_handler(commands='cmd_nivelss')
@dp.throttled(hello_throttled, rate=0)
async def cmd_nivelss(message: types.Message):
	await FormTNivel.value.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("0","1","2","3","4","5")
	await message.reply("Quantos nives?",reply_markup=markup)
	
@dp.message_handler(lambda message: message.text not in ["0","1","2","3","4","5"], state=FormTNivel.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeNivel_invalid(message: types.Message):
	return await message.reply("Quantos nives? escolha a opção no teclado")

@dp.message_handler(state=FormTNivel.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeNivel(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			if "cancelar" in message.text.lower():
				await message.reply("Cancelado", reply_markup=nav.mainMenu)
				await state.finish()
			else:
				data['value'] =message.text
				file.alterParameter(str(message.chat.id),'nivel',data['value'])
				await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
				await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)
		controlMessage.send_msg("BOTALLWINTELL-  FormTNivel.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
class FormFacGale(StatesGroup):
	factorGale = State()
@dp.message_handler(commands='cmd_fctociclos')
@dp.throttled(hello_throttled, rate=0)
async def cmd_fctogale(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("1.1","1.2","1.3")
	markup.add("1.4","1.5","1.6")
	markup.add("1.7","1.8","1.9","2.0")
	markup.add("2.1","2.2","2.3")
	markup.add("2.4","2.5","2.6")
	markup.add("2.7","2.8","2.9")
	await FormFacGale.factorGale.set()
	await message.reply("Qual fator do gale?",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["NÃO","SIM","0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.0","2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9"], state=FormFacGale.factorGale)
@dp.throttled(hello_throttled, rate=0)
async def process_typefactorGale_invalid(message: types.Message):
	return await message.reply("Qual fator do gale? escolha a opção no teclado")

@dp.message_handler(state=FormFacGale.factorGale)
@dp.throttled(hello_throttled, rate=0)
async def process_emgale(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['factorGale'] = message.text
			file.alterParameter(str(message.chat.id),'factorGale',data['factorGale'])
			await message.reply("Alterado para: "+str(data['factorGale']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)	
		controlMessage.send_msg("BOTALLWINTELL-  FormFacGale.factorGale "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
class FormTGale(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_sgale')
async def cmd_sgale(message: types.Message):
	await FormTGale.value.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("0","1","2","3","4","5")
	await message.reply("Quantos gales?",reply_markup=markup)
	

@dp.message_handler(lambda message: message.text not in ["0","1","2","3","4","5"], state=FormTGale.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Quantos gales? escolha a opção no teclado")

@dp.message_handler(state=FormTGale.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'gale',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)
		controlMessage.send_msg("BOTALLWINTELL-  FormTGale.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormTtrends(StatesGroup):
	value = State()
@dp.message_handler(commands='cmd_trend')
@dp.throttled(hello_throttled, rate=0)
async def cmd_trend(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("ON","OFF",'cancelar')
	await FormTtrends.value.set()
	await message.reply("Ativar análise de tendência?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["ON","OFF","Cancelar"], state=FormTtrends.value)
@dp.throttled(hello_throttled, rate=0)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Ativar análise de tendência? escolha a opção no teclado")

@dp.message_handler(state=FormTtrends.value)
@dp.throttled(hello_throttled, rate=0)
async def procesypeGale(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['value'] =message.text
			file.alterParameter(str(message.chat.id),'trend',data['value'])
			await message.reply("Alterado para: "+str(data['value']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  FormTtrends.value "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass
class FormFacCiclos(StatesGroup):
	factorCiclos = State()
@dp.message_handler(commands='cmd_fctociclos')
@dp.throttled(hello_throttled, rate=0)
async def cmd_fctociclos(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("1.1","1.2","1.3")
	markup.add("1.4","1.5","1.6")
	markup.add("1.7","1.8","1.9","2.0")
	markup.add("2.1","2.2","2.3")
	markup.add("2.4","2.5","2.6")
	markup.add("2.7","2.8","2.9","Cancelar")
	await FormFacCiclos.factorCiclos.set()
	await message.reply("Qual fator do ciclos?",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["NÃO","SIM","0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.0","2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9","Cancelar","SIM"], state=FormFacCiclos.factorCiclos)
@dp.throttled(hello_throttled, rate=0)
async def process_typefactorCiclos_invalid(message: types.Message):
	return await message.reply("Qual fator do ciclos? escolha a opção no teclado")

@dp.message_handler(state=FormFacCiclos.factorCiclos)
@dp.throttled(hello_throttled, rate=0)
async def process_emciclos(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			if "cancelar" in message.text.lower():
				await message.reply("Cancelado", reply_markup=nav.mainMenu)
				await state.finish()
			else:
				data['factorCiclos'] = message.text
				file.alterParameter(str(message.chat.id),'factorCiclos',data['factorCiclos'])
				await message.reply("Alterado para: "+str(data['factorCiclos']),reply_markup=nav.mainconfig)
				await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  FormFacCiclos.factorCiclos "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormStrategy(StatesGroup):
	strategy = State()
@dp.message_handler(commands='cmd_dasdstrategy')
@dp.throttled(hello_throttled, rate=0)
async def cmd_dasdstrategy(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("SorosGale", "Gale","Ciclos","Fixa")
	await message.reply("Qual tipo de gerenciamento para recuperação estou habilitado a usar hoje?",reply_markup=markup)
	await FormStrategy.strategy.set()

@dp.message_handler(lambda message: message.text not in ["SorosGale", "Gale","Ciclos","Fixa"] , state=FormStrategy.strategy)
@dp.throttled(hello_throttled, rate=0)
async def process_typed_invid(message: types.Message):
	return await message.reply('invalido, selecione uma opção de gerenciamento correta')


@dp.message_handler(state=FormStrategy.strategy)
@dp.throttled(hello_throttled, rate=0)
async def process_emstrar(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['strategy'] = message.text
			file.alterParameter(str(message.chat.id),'typeStrategy',data['strategy'])
			await message.reply("Alterado para: "+str(data['strategy']),reply_markup=nav.mainconfig)
		await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("ERRO:",reply_markup=nav.mainMenu)		
		controlMessage.send_msg("BOTALLWINTELL-  FormStrategy.strategy "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass


class FormDe(StatesGroup):
	delay = State()
@dp.message_handler(commands='cmd_delayt')
@dp.throttled(hello_throttled, rate=0)
async def cmd_delayt(message: types.Message):
	await FormDe.delay.set()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("1","2","3","4","5","6","7","8","9","10")
	await message.reply("Deseja antecipar o sinal em quantos segundos?\n\n(Os filtos de Payout e Touros interferem a primeira entrada no delay se  ativados e não é possivel ajusta o delay do gale)",reply_markup=markup)
	
@dp.message_handler(lambda message: message.text != validate.is_number(message.text) , state=FormDe.delay)
@dp.throttled(hello_throttled, rate=0)
async def process_typed_invalid(message: types.Message):
	return await message.reply('invalido, selecione uma opção do teclado para o delay')

@dp.message_handler(state=FormDe.delay)
@dp.throttled(hello_throttled, rate=0)
async def process_emdelay(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			if "cancelar" in message.text.lower():
				await message.reply("Cancelado", reply_markup=nav.mainMenu)
				await state.finish()
			else:
				data['delay'] = message.text
				file.alterParameter(str(message.chat.id),'delay',data['delay'])
				await message.reply("Alterado para: "+str(data['delay']),reply_markup=nav.mainconfig)
				await state.finish()
	except Exception as a:
		if 'No such file or directory' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg(" ERRO  1236 "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormSi(StatesGroup):
	sinais = State()
@dp.message_handler(commands='cmd_sinais')
@dp.throttled(hello_throttled, rate=0)
async def cmd_sinais(message: types.Message):
	try:
		await FormSi.sinais.set()
		conf  = file.get(str(message.chat.id))
		if conf['typeSignals'] == 'Meus Sinais':
			await message.reply('''Me envie a sua lista de ordens! - Formato:\n
	A lista não pode conter espaços no final: 
	\n
	M5;EURGBP-OTC;12:35:00;PUT
	M5;USDJPY-OTC;13:10:00;PUT
	M5;EURGBP-OTC;13:15:00;PUT
	M5;EURJPY-OTC;13:15:00;PUT
	\n
	após cada sinal, pular a linha sem espaço.''')
		else:
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
			markup.add("LISTA")
			await message.reply("ESCOLHA UMA SALA.",reply_markup=markup)
	except Exception as a:
		if 'No such file or directory' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg(" ERRO  1257 "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass


@dp.message_handler(lambda message: True != validate.listSigns(message.text) and message.text not in ["LISTA","OTC","M1","M5-24h","M15-24h","M30-24h","H1-24h"], state=FormSi.sinais)
@dp.throttled(hello_throttled, rate=0)
async def process_typed_invalid(message: types.Message):
	check, lista, reason = validate.datailsListSigns(message.text)
	if check == False:
		return await message.reply(reason)
	else:
		return await message.reply('há um erro')

@dp.message_handler(state=FormSi.sinais)
@dp.throttled(hello_throttled, rate=0)
async def process_emsinas(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['sinais'] = message.text
			if "cancelar" in message.text.lower():
				await message.reply("Cancelado", reply_markup=nav.mainMenu)
				await state.finish()
			else:
				conf  = file.get(str(message.chat.id))
				if conf['typeSignals'] == 'Meus Sinais':
					check,lists,reason = validate.datailsListSigns(message.text)
					if check :
						file.alterParameter(str(message.chat.id),'signals',lists)
						await message.reply("Alterado para:\n "+lists,reply_markup=nav.mainconfig)
					else:
						await message.reply("Há um erro: "+str(reason))
				else:
					file.alterParameter(str(message.chat.id),'signals',data['sinais'])
					await message.reply("Alterado para: "+str(data['sinais']),reply_markup=nav.mainconfig)

				await state.finish()
	except Exception as a:
		if 'No such file or directory' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg(" ERRO  1283 "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

class FormLogin(StatesGroup):
	email = State()
	passwd = State()
@dp.message_handler(commands='login')
@dp.throttled(hello_throttled, rate=0)
async def cmd_start(message: types.Message):
	if 0 ==1:#if connectDao.authenticateById(str(message.chat.id)) == False:
		await message.reply("Você não é um membro ")	
	else:
		await FormLogin.email.set()
		await message.reply("Oi {0}, eu sou o Bot. vamos lá, qual seu email de acesso à corretora?".format(message.chat.first_name))

@dp.message_handler(state=FormLogin.email)
@dp.throttled(hello_throttled, rate=0)
async def process_email(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['email'] = message.text
	await FormLogin.next()
	await message.reply("Isso ai {0} agora preciso da sua senha para que eu possa me conectar à sua conta.".format(message.chat.first_name))
		
@dp.message_handler(state=FormLogin.passwd)
@dp.throttled(hello_throttled, rate=0)
async def process_passwds(message: types.Message, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['passwd'] = message.text
			key = Fernet.generate_key()
			f = Fernet(key)
			passwd = str(f.encrypt(bytes(data['passwd'], 'utf-8')))
			passwd = str(passwd[2:-1])
			Key = str(key)
			Key = str(Key[2:-1])

			validate.verifyIQ(data['email'], data['passwd'],str(message.chat.id),Key,passwd)
			user = file.get(message.chat.id)
			if user:
				if "cancelar" in message.text.lower():
					await message.reply("Cancelado > /start/config")
					await state.finish()
				elif user["valid"] == "True":
					await message.reply("OK, Salvo! Agora configure seu bot -> ⚙️")
					await state.finish()
				else:
					await message.reply("Dados da IQ estão incorretos ou conta não está ativa")
					await state.finish()
			else:
				await message.reply("Dados da IQ estão incorretos: Envie /start após isso tente o login")
				await state.finish()
	except Exception as a:
		await state.finish()
		await message.reply("Dados da IQ estão incorretos")
		controlMessage.send_msg("BOTALLWINTELL- FormLogin.passwd "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

@dp.message_handler(commands='stop')
@dp.throttled(hello_throttled, rate=0)
async def cmd_sstop(message: types.Message):
	try:
		conf  = file.get(str(message.chat.id))
		if conf['start'] == 'True':
			file.alterParameter(str(message.chat.id),'start',False)
			conf  = file.get(str(message.chat.id))
			if conf['start'] == 'False':
				await bot.send_message(message.chat.id,'Parando',parse_mode=ParseMode.HTML)
		else:
			await bot.send_message(message.chat.id,'Já está parado',parse_mode=ParseMode.HTML)
	except Exception as a:
		if 'No such file or directory' in str(a) or 'object is not subs' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			try:
				file.alterParameter(str(message.chat.id),'start',False)
			except:
				pass
			controlMessage.send_msg(" ERRO  stop "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

@dp.message_handler(commands='cmd_sdfinsihs')
@dp.throttled(hello_throttled, rate=0)
async def cmd_sdfinsihs(message: types.Message):
	try:
		conf  = file.get(str(message.chat.id))
		if conf['finish'] == 'False':
			file.alterParameter(str(message.chat.id),'finish',True)
			file.alterParameter(str(message.chat.id),'start',False)
			conf  = file.get(str(message.chat.id))
			if conf['finish'] == 'True':
				await bot.send_message(message.chat.id,'Finalizando...aguarde',parse_mode=ParseMode.HTML)
		else:
			await bot.send_message(message.chat.id,'Já está finalizado',parse_mode=ParseMode.HTML)
	except Exception as a:
		if 'No such file or directory' in str(a):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+"\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg(" ERRO:  sair e desconectar "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
			try:
				file.alterParameter(str(message.chat.id),'finish',True)
				file.alterParameter(str(message.chat.id),'start',False)
			except:
				pass
		pass

@dp.message_handler(commands='goGARRATRANDING')
@dp.throttled(hello_throttled, rate=0)
async def cmd_startwin(message: types.Message):
	if 0 ==1:#if connectDao.authenticateById(str(message.chat.id)) == False:
		await message.reply("Você não é um membro ",reply_markup=nav.mainMenu)	
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		try:
			markup.add("REAL","TORNEIO","PRATICA","Cancelar")
			await FormGo.cods.set()
			await message.reply("Onde devo agendar?",reply_markup=markup)
		except Exception as a:
			controlMessage.send_msg("BOTALLWINTELL "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
			pass
	
@dp.message_handler(state=FormGo.cods)
@dp.throttled(hello_throttled, rate=0)
async def process_cods(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		markup = nav.mainMenu
		data['cods'] = message.text
	if 0 ==1:#if connectDao.authenticateById(str(message.chat.id)) == False:
		await message.reply("Você não é um membro ",reply_markup=markup)
		await state.finish()
	if data['cods'].lower() == 'cancelar':
		await message.reply("Cancelado ",reply_markup=markup)
		await state.finish()
	else:
		try:
			conf  = file.get(str(message.chat.id))
			if conf == False:
				await bot.send_message(message.from_user.id, "Você deve primeiro enviar o comando \start e '👤' Login. Você não tem uma configuração ativa", reply_markup = nav.mainMenu) 
			else:
				if data['cods'] in ["PRATICA","TORNEIO","REAL","Cancelar"]:
					file.alterParameter(str(message.chat.id),'typeAcc',data['cods'])
					await bot.send_message(message.chat.id,MENSAGE.MSG002.value,parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
					await message.reply("🤖:Alterado para "+data['cods'].upper(),reply_markup=nav.mainMenu)
					if conf['start'] == "False":
						file.alterParameter(str(message.chat.id),'start',True)
						conf  = file.get(str(message.chat.id))
						t = Process(target=comand.start, args=(message.chat.id,API_TOKEN),daemon=True)
						t.start()
						file.alterParameter(str(message.chat.id),'PID',str(t.pid))
					else:
						await bot.send_message(message.chat.id,'Já esta em execução. ID:'+str(conf['PID'])+'\nEnvie: ⏸\nem seguida...\n▶️ Inciar ',parse_mode=ParseMode.HTML)
					await state.finish()
				else:
					await message.reply("🤖:Opção invalida  - /config",reply_markup=nav.mainMenu)
					await state.finish()
		except Exception as a:
			if 'No such file or directory' in str(a):
				await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
			else:
				controlMessage.send_msg("BOTALLWINTELL- FormGo.cods 	 "+str(message.chat.id)+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
			await state.finish()
			pass



@dp.message_handler(commands='stops')
@dp.throttled(hello_throttled, rate=0)
async def cmd_ssssteset(message: types.Message):
	try: 
		namfile = message.text.split(' ')[1]
		conf  = file.get(str(namfile))
		if conf:
			file.alterParameter(str(namfile),'start',False)
			pid = conf['PID']
			try:
				os.kill(int(pid), signal.SIGTERM)
				os.kill(int(pid), 0)
			except:
				pass
	except Exception as ex:
		if 'Errno 3] No such pro' in str(ex):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nNã há sinais agendados ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg("ALLWINBOT- reset "+str(namfile)+str(ex), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

@dp.message_handler(commands='reset')
@dp.throttled(hello_throttled, rate=0)
async def cmd_steset(message: types.Message):
	try: 
		conf  = file.get(message.chat.id)
		if conf:
			pid = conf['PID']


			try:
				os.kill(int(pid), signal.SIGTERM)
				os.kill(int(pid), 0)
				os.remove(str(message.chat.id)+".txt")
			except:
				try:
					os.remove(str(message.chat.id)+".txt")
				except:
					pass
				pass
	except Exception as ex:
		if 'No such file or directory' in str(ex):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		elif 'Errno 3] No such pro' in str(ex):
			await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nNã há sinais agendados ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
		else:
			controlMessage.send_msg("ALLWINBOT- reset "+str(message.chat.id)+str(ex), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		pass

@dp.message_handler(commands=['savess'])
@dp.throttled(hello_throttled, rate=0)
async def command_saveconf(message: types.Message):
	id = str(message.chat.id)
	if os.path.exists(str(id)+'.txt'):
		check, conf = file.getDif(str(id))
		if check:
			check, reason = connectDao.saveData(conf,str(id))
			if check:
				await bot.send_message(message.chat.id,str(id)+' - '+str(message.chat.username)+': Salvo!', reply_markup = nav.mainMenu)
			else:
				if reason !='':
					controlMessage.send_msg("ALLWINBOT- command_saveconf "+str(message.chat.id)+str(reason), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				await bot.send_message(message.chat.id,'Não foi possivel salvar', reply_markup = nav.mainMenu)
		else:
			await bot.send_message(message.chat.id,'Não foi possivel salvar', reply_markup = nav.mainMenu)
	else:
		await bot.send_message(message.chat.id,'Não foi possivel salvar', reply_markup = nav.mainMenu)

@dp.message_handler(commands='sendmsg')	
@dp.throttled(hello_throttled, rate=0)
async def cmd_tt(message: types.Message):
	if str(message.chat.id) in ['971655878']:
		await sendmsg.msg.set()
		await message.reply("{0}, qual a mensagem?".format(message.from_user.first_name))
	else:
		await message.reply("{0}, Você recebeu uma advertencia e foi reportado para o suporte:".format(message.from_user.first_name))


@dp.message_handler(state=sendmsg.msg)
@dp.throttled(hello_throttled, rate=0)	
async def procs_serco(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		if 'cancelar' in message.text.lower():
			markup = nav.mainMenu
			await message.reply("Ok, Cancelado")
			await state.finish()
		else:
			data['msg'] = message.text
			markup = nav.mainMenu
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
			markup.add("SIM","NÃO")
			await sendmsg.next()
			await message.reply("Posso enviar?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["SIM","NÃO","cancelar"], state=sendmsg.finish)
async def proces_typetouro_invalid(message: types.Message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("SIM","NÃO","CANCELAR")
	await message.reply(message.chat.id,'escolha a opção no teclado',reply_markup=markup)

@dp.message_handler(state=sendmsg.finish)
async def proces_FINSH(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['finish'] = message.text
		markup = nav.mainMenu
		if data['finish'] == "SIM":
			try:
				valid, Users = connectDao.selUsers()
				if valid:
					for user in Users:
						time.sleep(0.2)
						threading.Thread(target=controlMessage.send_msg, args=(str(data['msg']),str(user[0]),API_TOKEN), daemon=True).start()
					await state.finish()
				else:
					controlMessage.send_msg(message.chat.id,'ERRO USER',parse_mode=ParseMode.HTML)
					await state.finish()
					
			except Exception as a:
				controlMessage.send_msg(" ERRO  sendmsg "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				await state.finish()
				pass

		else:
			await message.reply("Ok, encerrado")
			await state.finish()


@dp.message_handler(commands='helplist')
@dp.throttled(hello_throttled, rate=0)	
async def cmd_starlis(message: types.Message):
	t = '''
	A lista não pode conter espaços no final: 
	\n
	M5;EURGBP-OTC;12:35:00;PUT
	M5;USDJPY-OTC;13:10:00;PUT
	M5;EURGBP-OTC;13:15:00;PUT
	M5;EURJPY-OTC;13:15:00;PUT
	\n
	após cada sinal, pular a linha sem espaço.
	'''
	await bot.send_message(message.chat.id,t,parse_mode=ParseMode.HTML)
@dp.message_handler(commands='myconf')
@dp.throttled(hello_throttled, rate=0)	
async def cmd_t(message: types.Message):
	if True:
	#try:
		text = ''
		piy = ''
		conf  = file.get(str(message.chat.id))
		if conf == False:
			await bot.send_message(message.from_user.id, "Você deve primeiro enviar o comando \start e '👤' Login. Você não tem uma conta ativa", reply_markup = nav.mainMenu) 
		else:
			for a in conf:
				if a == 'invest' or  a == 'stopWin' or  a == 'stopLoss':
					spp = conf[a].split('.')
					piy = "R$/$ {0}".format(spp[0]+",00")
					if str(conf['typeEnter']) == "%":
						piy = "{0}%"
				if a == 'email':
					text += '<b>Email</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'    
				elif a == 'typeStrategy':
					text += '<b>Tipo de estratégia</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'trend':
					text += '<b>Tendência</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'gale': 
					text += '<b>Gale</b>: '   
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'   
				elif a == 'factorGale': 
					text += '<b>Fator do Gale</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'nivel':      
					text += '<b>Nivel</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'factorCiclos':
					text += '<b>Fator do ciclos</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'delay':
					text += '<b>Delay</b>: ' 
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'preStop':    
					text += '<b>Pré Stop</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'doji':       
					text += '<b>Pós Doji</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'typeEnter':
					text += '<b>Tipo de Entrada</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'invest':     
					text += '<b>Entrada</b>: '
					text +=piy.format( str(conf[a]))+'\n' 
				elif a == 'stopWin':   
					text += '<b>Stop Win</b>: '
					text +=piy.format( str(conf[a]))+'\n' 
				elif a == 'stopLoss': 
					text += '<b>Stop Loss</b>: '
					text +=piy.format(str(conf[a]))+'\n' 
				elif a == 'typeSignals':
					text += '<b>Tipo de Sala</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'date':      
					text += '<b>Data</b>: '  
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'typeAcc':
					text += '<b>Conta</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'touros':
					text += '<b>Nível de touros</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'maxSim':
					text += '<b>Max. Simutâneas</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'pay':
					text += '<b>PayOut</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
				elif a == 'PID':
					text += '<b>ID-EXE</b>: '
					text +='OFF'+'\n' if conf[a] == False else 'ON'+'\n' if conf[a] == True else str(conf[a])+'\n'
			controlMessage.send_msg(text, message.chat.id,API_TOKEN)
			txt = '<b>Sinais</b>: '
			txt +='OFF'+'\n' if conf['signals'] == False else 'ON'+'\n' if conf['signals'] == True else str(conf['signals'])+'\n'
			controlMessage.send_msg(txt, message.chat.id,API_TOKEN)
		

	#except Exception as a:
	#	if 'No such file or directory' in str(a):
	#		await bot.send_message(message.chat.id,MENSAGE.MSG008.value.format(message.chat.first_name)+".\nVocê deve primeiro enviar o comando \start ou '👤'  - analise sua configuração de conta em '📚 Informação' ",parse_mode=ParseMode.HTML,reply_markup=nav.mainMenu)
	#	else:
	#		controlMessage.send_msg(" ERRO  infomações "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
	#	pass
@dp.message_handler()
@dp.throttled(hello_throttled, rate=0)	
async def bot_message(message: types.Message):
	# await bot.send_message(message.from_user.id, message.text) 
	if message.text == '👤':
		await cmd_start(message)
	elif message.text == '🔩 Fator do ciclos':
		await cmd_fctociclos(message)
	elif message.text == '🔩 Tendência':      
		await cmd_trend(message)
	elif message.text == '🔩 Delay':
		await cmd_delayt(message)
	elif message.text == '🔩 Estratégia':     
		await cmd_dasdstrategy(message)
	elif message.text == '🔩 Gale':
		await cmd_sgale(message)
	elif message.text == '🔩 Fator do Gale':  
		await cmd_fctogale(message)
	elif message.text == '🔩 Nivel':
		await cmd_nivelss(message)
	elif message.text == '🔩 Pré Stop':       
		await cmd_stprestop(message)
	elif message.text == '🔩 Pós Doji':       
		await cmd_stpredoji(message)
	elif message.text == '🔩 Entrada':        
		await cmd_sinves(message)
	elif message.text == '🔩 Stop Win':       
		await cmd_sstopWin(message)
	elif message.text == '🔩 Stop Loss':      
		await cmd_sstopLoss(message)
	elif message.text == '🔩 Tipo de Sala':   
		await cmd_stypeSignals(message)
	elif message.text == '🔩 Sinais':
		await cmd_sinais(message)
	elif message.text == '🔩 Data':
		await cmd_sdataess(message)
	elif message.text == '🔩 Touros':
		await cmd_sTouros(message)
	elif message.text == '🔩 Max. Simutâneas':
		await cmd_Mmax(message)
	elif message.text == '🔩 Tipo de Entrada':
		await cmd_stpretypeEnter(message)
	elif message.text == '🔩 PayOut':
		await cmd_fcpayou(message)
	elif message.text == '▶️':
		await cmd_startwin(message)
	elif message.text == '⏸':
		await cmd_sstop(message)
	elif message.text == '♻️':
		conf  = file.get(message.chat.id)
		if conf:
			await cmd_steset(message)
		else:
			await bot.send_message(message.from_user.id, "Você deve primeiro enviar o comando \start ou '👤 você não tem uma conta ativa", reply_markup = nav.mainMenu)
	
	#elif message.text  ==	'🗂':
	#	conf  = file.get(message.chat.id)
	#	if conf:
	#		await command_saveconf(message)
	#	else:
	#		await bot.send_message(message.from_user.id, "Você deve primeiro enviar o comando \start ou '👤 você não tem uma conta ativa", reply_markup = nav.mainMenu)
	
		

	elif message.text == '⚙️':
		conf  = file.get(message.chat.id)
		if conf:
			await cmd_strategy(message)
		else:
			await bot.send_message(message.from_user.id, "Você deve primeiro enviar o comando \start ou '👤 você não tem uma conta ativa", reply_markup = nav.mainMenu)
	
	elif message.text == '🛠':
		conf  = file.get(message.chat.id)
		if conf:
			await bot.send_message(message.from_user.id, "Escolha uma opção para alterar", reply_markup = nav.mainconfig) 
		else:
			await bot.send_message(message.from_user.id, "Você deve primeiro enviar o comando \start ou '👤 você não tem uma conta ativa", reply_markup = nav.mainMenu) 
	elif message.text == '🌐':
		await bot.send_message(message.from_user.id, "🌐", reply_markup = nav.mainMenu) 

	elif message.text == '📑':
		await cmd_t(message) 	
	else:
		await message.reply('Oi, Redirecione para menu com /start')

if __name__ == '__main__':
	try:
		start_polling(dp, skip_updates=True)
	except Exception as a:
		controlMessage.send_msg("start_polling"+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
		
		pass