from random import choice
from iqoptionapi.constants import ACTIVCATALAGVip,acc,Activ
from Controller.controlCatalog import controlCatalog,MsgTo
from Controller.controlCatalogTo import controlCatalogTo
from ControllerTo.controlCatalog import controlCatalogTre
from Controller.controlConfig import controlValue
from iqoptionapi.stable_api import IQ_Option
from Controller.controlConfig import controlParameter
import nav 
import threading
from Controller.ControlReg import Reg
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
import logging, requests,json
from Controller.controlDao import connectDao
from Controller.controlConfig import ControlCheck
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from Controller.controlEnum import MENSAGE,MENSAGE_ERRO
from telegram import ParseMode
#logger = logging.getLogger()
#logger.disabled = False
logging.basicConfig(level=logging.INFO)
M5LI = ["TODOS",'MHI','FORÇA MENOR 15','TORRES GÊMEAS','NÃO TRIPLICAÇÃO' '3 VIZINHOS','TRIPLICAÇÃO','MILHÃO MAIORIA','MILHÃO MINORIA']
M1LI= ["TODOS",'MELHOR DE 3','MILHÃO MAIORIA','MILHÃO MINORIA',"MHI-MAIORIA","MHI","MHI-2", "MHI-3","TORRES GÊMEAS","PADRÃO 23","5º ELEMENTO","PADRÃO 3 X 1","3 VIZINHOS","3 MOSQUETEIROS"]
ALLLI = ["TODOS",'cancelar','MELHOR','MELHOR DE 3','MILHÃO MAIORIA','MILHÃO MINORIA',"MHI-MAIORIA","MHI","MHI-2", "MHI-3","TORRES GÊMEAS","PADRÃO 23","5º ELEMENTO","PADRÃO 3 X 1","3 VIZINHOS","3 MOSQUETEIROS",'MHI','FORÇA MENOR 15','TORRES GÊMEAS','NÃO TRIPLICAÇÃO' '3 VIZINHOS','TRIPLICAÇÃO','MILHÃO MAIORIA','MILHÃO MINORIA']
M15LI = ["TODOS","MHI-MAIORIA","MHI","TORRES GÊMEAS"]

API_TOKEN = '6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM'
API=IQ_Option("ridev97046@whyflkj.com","j3100davi")
API.connect()
API.change_balance("PRACTICE")
API.check_connect()
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def is_number(d):
	try:
		int(d)
		return d
	except ValueError:
		return False
	except TypeError:
		return False
def is_float(d):
	try:
		float(d)
		return d
	except ValueError:
		return False
	except TypeError:
		return False
def is_time(d):
	try:
		s  = d.split(' ')
		for a in s:
			if int(a) > 60 and int(a) <= 0:
				return False
		return d
	except ValueError:
		return False
	except TypeError:
		return False
def is_par(d):
	try:
		s = d.split(' ')
		for a in s:
			if a not in Activ:
				return False
		return d
	except ValueError:
		return False
	except TypeError:
		return False

class Trends(StatesGroup):
	pair = State()
	time = State()
	candles = State()
	finish = State()
class Cat(StatesGroup): 
	dias = State()
	gale = State()
	analysePct = State()
	trend = State()
	trendPct = State()
	pairs = State()
	time = State()
	date = State()
	dir = State()
	finish = State()
class Check(StatesGroup):
	gale = State()
	date = State()
	signals = State()
	finish = State()



def is_parr(d):
	try:
		s = d.split(',')
		for a in s:
			if a not in Activ:
				return False
		return d
	except ValueError:
		return False
	except TypeError:
		return False

class Cato(StatesGroup): 
	dias = State()
	gale = State()
	analysePct = State()
	pairs = State()
	notici = State()
	minNot = State()
	time = State()
	finish = State()
class FormCalc(StatesGroup):
	types = State()
	input =  State()
class FormJuros(StatesGroup):
	input = State()
	banca = State()
	days = State()
class Formsig(StatesGroup):
	email = State()
	senha = State()
	finish = State()

class sendmsg(StatesGroup):
	msg = State()
	finish = State()
@dp.message_handler(commands='adminmsg44')	
async def cmd_tt(message: types.Message):
	await sendmsg.msg.set()
	await message.reply("{0}, qual a mensagem?".format(message.from_user.first_name))

@dp.message_handler(state=sendmsg.msg)
async def procs_serco(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		if 'cancelar' in message.text.lower():
			markup = types.ReplyKeyboardRemove()
			await message.reply("Ok, Cancelado")
			await state.finish()
		else:
			data['msg'] = message.text
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
		markup = types.ReplyKeyboardRemove()
		if data['finish'] == "SIM":
			try:
				valid, Users = connectDao.selUsers()
				if valid:
					for user in Users:
						time.sleep(0.2)
						threading.Thread(target=MsgTo.send_msg, args=(str(data['msg']),str(user[0]),API_TOKEN), daemon=True).start()
					await state.finish()
				else:
					MsgTo.upload_file (message.chat.id,'ERRO USER',parse_mode=ParseMode.HTML)
					await state.finish()
					
			except Exception as a:
				await message.reply('ERRO: Contate o suporte com o erro: '+str(a),reply_markup=markup)
				await state.finish()
				pass

		else:
			await message.reply("Ok, encerrado")
			await state.finish()


@dp.message_handler(commands='admin33')
async def cmd_start(message: types.Message):
	await Formsig.email.set()
	await message.reply("Qual ID do user e o nome EX: 123445,davi?".format(message.chat.first_name))


@dp.message_handler(state=Formsig.email)	
async def process_semail(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['email'] = message.text
	await Formsig.next()
	await message.reply("Qual data de vencimento(teste 2 dias, mensal 30 dias)???".format(message.chat.first_name))

@dp.message_handler(state=Formsig.senha)
async def process_optionsdateTop(message: types.Message, state: FSMContext):
	markup = types.ReplyKeyboardRemove()
	async with state.proxy() as data:
		data['senha'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("Ok, cancelado")
		await state.finish()
	else:
		sig, a = connectDao.insertAcc(data['email'], data['senha'] )
		if sig:
			await message.reply("OK\n\nAtivo",reply_markup=markup)
		else:
			await message.reply(a,reply_markup=markup)
	await state.finish()


@dp.message_handler(commands='gerenciamento')
async def cmd_gerenciamento(message: types.Message):
	try:
		MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o gerenc", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
		if True:
			await FormCalc.types.set()
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
			markup.add("Ciclos", "SorosGale","Gale","Cancelar")
			await message.reply("Qual tipo de calculadora deseja simular? Ciclos, Gale, SorosGale?",reply_markup=markup)
		else:
			await message.reply("Usuario não está ativo")
	except Exception as a:
		await message.reply("ERRO: {0} ".format(str(a)))
		
@dp.message_handler(state=FormCalc.types)
async def process_types(message: types.Message, state: FSMContext):
	markup = types.ReplyKeyboardRemove()
	async with state.proxy() as data:
		data['types'] = message.text
	if data['types'].lower() == 'cancelar':
		await message.reply("Cancelado  ")
		await state.finish()
	else:
		try:
			await message.reply("Qual valor da sua entrada(R$)?",reply_markup=markup)
			await FormCalc.next()
		except Exception as a:
			await bot.send_message('ERRO',parse_mode=ParseMode.HTML,reply_markup=markup)
			await state.finish()
			pass
	
@dp.message_handler(lambda message: is_float(message.text) == False, state=FormCalc.input)
async def process_types_invalid(message: types.Message):
	return await message.reply("Invalido,Qual valor da sua entrada?")

@dp.message_handler(state=FormCalc.input)
async def process_input(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['input'] = message.text
	if data['input'].lower() == 'cancelar':
		await message.reply("Cancelado  ")
		await state.finish()
	else:
		try:
			if "Ciclos" == data['types']:
				await message.reply(controlValue.CalcCi(data['input']))
			elif "SorosGale" == data['types']:
				await message.reply(controlValue.CalcSo(data['input']))
			else:
				await message.reply(controlValue.CalcGal(data['input']))
			await state.finish()
		except Exception as a:
			await bot.send_message('ERRO',parse_mode=ParseMode.HTML)
			await state.finish()
			pass


@dp.message_handler(commands='jurosc')
async def process_jurosc(message: types.Message):
	try:
		MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o jurosc", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
		if True:
			await FormJuros.input.set()
			await message.reply("Qual porcentagem de lucro diario?(%)")
		else:
			await message.reply("Usuario não está ativo")
	except Exception as a:
		await message.reply("ERRO: {0} ".format(str(a)))



@dp.message_handler(lambda message: is_float(message.text) == False, state=FormJuros.input)
async def process_input_invalid(message: types.Message):
	return await message.reply("Invalido, Qual porcentagem de lucro diario?")

		
@dp.message_handler(state=FormJuros.input)
async def process_input(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['input'] = message.text
	if data['input'].lower() == 'cancelar':
		await message.reply("Cancelado  ")
		await state.finish()
	else:
		await FormJuros.next()
		await message.reply("Qual valor da conta?")
@dp.message_handler(lambda message: is_float(message.text) == False, state=FormJuros.banca)
async def process_banca_invalid(message: types.Message):
	return await message.reply("Invalido, Qual valor da conta?")
@dp.message_handler(state=FormJuros.banca)
async def process_banca(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['banca'] = message.text
	if data['banca'].lower() == 'cancelar':
		await message.reply("Cancelado  ")
		await state.finish()
	else:
		await FormJuros.next()
		await message.reply("Quantos dias?")




@dp.message_handler(lambda message: is_number(message.text) == False, state=FormJuros.days)
async def process_banca_invalid(message: types.Message):
	return await message.reply("Invalido, Quantos dias?")




@dp.message_handler(state=FormJuros.days)
async def process_banca(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['days'] = message.text
	if data['days'].lower() == 'cancelar':
		await message.reply("Cancelado  - /jurosc")
		await state.finish()
	else:
		try:
			await message.reply(controlValue.jurosCom(float(data['banca']),float(data['input']),int(data['days'])))
			await state.finish()
		except Exception as a:
			await message.reply('ERRO '+str(a))
			await state.finish()



###############CATALOOOOG####################
@dp.message_handler(commands='CTGs')
async def cmd_sgales(message: types.Message):
	MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o CT SINAIS II", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
	
	if True:
		await Cato.dias.set()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add('1','2','3','4','5','6','7','8','9','10','cancelar')
		await message.reply("🤖Ok {0}\nQuantos dias?".format(message.from_user.first_name),reply_markup=markup)
	else:
		await message.reply("🤖{0}\n\nSó Membro".format(message.from_user.first_name)) 
		await message.reply(MENSAGE.ALL.value +"\nID:"+str(message.chat.id),parse_mode=ParseMode.HTML)
	

@dp.message_handler(lambda message: message.text != is_number(message.text) , state=Cato.dias)
async def process_typefiltro_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido,Quantos dias?',parse_mode=ParseMode.HTML)



@dp.message_handler(state=Cato.dias)
async def process_touro(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['dias'] = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("0","1","cancelar")
	if "cancelar" in message.text.lower():
		await message.reply("🤖Ok, cancelado")
		await state.finish()
	else:
		await Cato.next()
		await message.reply("🤖Ok\n\nQuantos gales?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["0","1","cancelar"], state=Cato.gale)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Invalido, escolha gale no teclado")

@dp.message_handler(state=Cato.gale)
async def process_typeGale(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['gale'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🤖Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("50","51","52","53","54","55","56","57","58","0",
		"60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99","100","cancelar")
		await Cato.next()
		await message.reply("🤖Ok\n\nqual porcentagem minima da análise?",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["50","51","52","53","54","55","56","57","58","0","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","cancelar"], state=Cato.analysePct)
async def process_typeanalysePct_invalid(message: types.Message):
	return await message.reply("Invalido, escolha a opção no teclado")


@dp.message_handler(state=Cato.analysePct)
async def process_analysePct(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['analysePct'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🤖Ok, cancelado")
		await state.finish()
	else:
		await Cato.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add('cancelar')
		for par in Activ:
			markup.add(par)	
		await message.reply("🤖OK\n\nquais pares?\nSepare com virgula, ex: EURUSD,EURAUD",reply_markup=markup)
	
@dp.message_handler(lambda message: message.text != is_parr(message.text), state=Cato.pairs)
async def process_typedate_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido, quais pares?',parse_mode=ParseMode.HTML)


@dp.message_handler(state=Cato.pairs)
async def process_trendpct(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['pairs'] = message.text
	if "Cancelar" in message.text:
		await message.reply("Cancelado ",reply_markup=markup)
		await state.finish()
	else:
		await Cato.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO","Cancelar")
		await message.reply("Analisar Noticia?",reply_markup=markup)
	

@dp.message_handler(lambda message: message.text not in ["NÃO","Cancelar","SIM"], state=Cato.notici)
async def process_typeGanvalid(message: types.Message):
	return await message.reply("Quantos gales? escolha a opção no teclado")

@dp.message_handler(state=Cato.notici)
async def process_tGale(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['notici'] = message.text
	if "Cancelar" in message.text:
		markup = nav.mainMenu
		await message.reply("Cancelado ",reply_markup=markup)
		await state.finish()
	elif data['notici'] == 'NÃO':
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		await Cato.next()
		markup.add("SIM","NÃO")
		await message.reply("Posso prosseguir?",reply_markup=markup)
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("10","15","30","40")
		await Cato.next()
		await message.reply("Quantos minutos?(antes e depois)",reply_markup=markup)	
		

@dp.message_handler(lambda message: message.text not in ["10","15","30","40",'NÃO','SIM'], state=Cato.minNot)
async def process_tyvel_invalid(message: types.Message):
	return await message.reply("Quantos minutos? escolha a opção no teclado")

@dp.message_handler(state=Cato.minNot)
async def process_typeGe(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['minNot'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🤖Ok, cancelado")
		await state.finish()
	if "NÃO" in message.text:
		await message.reply("🤖Ok, cancelado")
		await state.finish()
	else:
		await Cato.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","5","15","60","cancelar")
		await message.reply("🤖OK\n\nQual timeframe?",reply_markup=markup)
	
@dp.message_handler(lambda message: message.text not in ["1","5","15","60"], state=Cato.time)
async def process_typedate_lid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido, Qual timeframe?',parse_mode=ParseMode.HTML)

@dp.message_handler(state=Cato.time)
async def process_trendpct(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['time'] = message.text

	if "cancelar" in message.text.lower():
		await message.reply("🤖Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO")
		await Cato.next()
		await message.reply("OK\n\nPosso iniciar?",reply_markup=markup)

@dp.message_handler(state=Cato.finish)
async def process_FINSH(message: types.Message, state: FSMContext):
	global API_TOKEN
	async with state.proxy() as data:
		data['finish'] = message.text
		markup = nav.mainMenu
		if data['finish'] == "SIM":
			await bot.send_message(message.chat.id,'Ok, vou analisar pra você calma ai ja volto😜😋. aguarde o tempo é conforme o pedido e eu ainda não sou flash😜.',parse_mode=ParseMode.HTML,reply_markup=markup)
			arqname = str(datetime.now())
			arqname = arqname.replace(".","")
			arqname = arqname.replace(" ","")
			arqname = arqname.replace(":","")
			arqname = arqname.replace("-","")
			arqname = str(message.from_user.first_name)+"#"+arqname	
			conf = {'porcentagem_mao_fixa': int(data['analysePct']), 'porcentagem_gale': int(data['analysePct']), 'pares': data['pairs'].split(','), 'dias_analise': int(data['dias']), 'timeframe_analise': int(data['time']), 'martingale': int(data['gale'])}			
			threading.Thread(target=controlCatalogTo.catalog, args=(API,conf,arqname,message.chat.id,API_TOKEN,data['notici'],data['minNot']), daemon=True).start()
			
		else:
			await message.reply("🤖Ok {0}, para começar novamente cique em /CTG".format(message.from_user.first_name),reply_markup=markup)
	await state.finish()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
	#check = False#check, ids  = connectDao.selectIds(str(message.from_user.id))
	#if check:
	#	checks = connectDao.registeIrd(str(message.from_user.id))
	markup = nav.mainMenu
	MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o Tools", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
	await bot.send_message(message.chat.id,'''🤖: Bem Vindo
OS COMANDOS SÃO:

📊TENDÊNCIA📊 (Analisar a tendência do mercado força compradora ou vendedora)

📝CHECK LIST📝(Fazer checkin de win, loss e doji de qualquer hora e dia existente)

📡NOTÍCIAS📡(Saber as notiícias do mercado para uma melhor assertividade nas operações)

🔰CATALOGAR SINAIS🔰(Faça sua Propria lista de sinais para usar ou sua sala de sinais)

🔰CATALOGAR SINAIS II🔰(Faça sua Propria lista de sinais para usar ou sua sala de sinais)

🔢CALCULADORAS🔢(Saiba como será as operações de Sorosgale, Gale e Ciclos)

🔣JUROS C.🔣(Calcule seu lucro baseado em juros compostos saiba como será o seu futuro seguindo gerenciamento) ''',parse_mode=ParseMode.HTML,reply_markup=markup)

@dp.message_handler(commands='tnd')
async def cmd_start(message: types.Message):
	global API
	threading.Thread(target=Reg.bb,args=(0,API),daemon=True).start()
	await bot.send_message(message.chat.id,'pasando',parse_mode=ParseMode.HTML)



@dp.message_handler(commands='TRD')
async def cmd_fctociclos(message: types.Message):
	
	MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o TRD", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
	
	if True:
		await Trends.pair.set()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add('BTCUSD','EOSUSD','ETHUSD','LTCUSD','XRPUSD','EURUSD','EURGBP','GBPJPY','EURJPY','GBPUSD','USDJPY','AUDCAD','NZDUSD','USDCHF','EURUSD-OTC','EURGBP-OTC','USDCHF-OTC','EURJPY-OTC','NZDUSD-OTC','GBPUSD-OTC','GBPJPY-OTC','USDJPY-OTC','AUDCAD-OTC','AUDUSD','USDCAD','AUDJPY','GBPCAD','GBPCHF','GBPAUD','EURCAD','CADCHF','EURAUD','EURNZD','AUDCHF','AUDNZD','CADJPY','EURCHF','GBPNZD','NZDCAD','NZDJPY','NZDCHF','cancelar')
		await message.reply("🦁:Ok {0}\n\nEscolha uma paridade ou para saber a tendencia.".format(message.from_user.first_name),reply_markup=markup)
	else:
		await message.reply("🦁:{0}\n\nSó Membro".format(message.from_user.first_name)) 
		await message.reply(MENSAGE.ALL.value +"\nID:"+str(message.chat.id),parse_mode=ParseMode.HTML)

@dp.message_handler(lambda message: message.text not in ACTIVCATALAGVip, state=Trends.pair)
async def process_typepair_invalid(message: types.Message):
	return await message.reply("escolha a opção no teclado")


@dp.message_handler(state=Trends.pair)
async def process_pair(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		if message.text == "Todos":
			data['pair'] = None
		else:
			data['pair'] = message.text
	if 'cancelar' == message.text.lower():
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","60","cancelar")
		await Trends.next()
		await message.reply("🦁:OK\n\n Você quer que eu analiso em que tempo(minutos)",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","60","cancelar"], state=Trends.time)
async def process_typetouros_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido,Você quer que eu analiso em que tempo(minutos)"',parse_mode=ParseMode.HTML)


@dp.message_handler(state=Trends.time)
async def process_touro(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['time'] = message.text
	if 'cancelar' in  message.text.lower():
		await state.finish()
	else:
		await Trends.next()
		await message.reply("🦁:OK\n\nQuantas velas?")

@dp.message_handler(lambda message: message.text != is_number(message.text) , state=Trends.candles)
async def process_typefiltro_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido, Quantas velas?',parse_mode=ParseMode.HTML)


@dp.message_handler(state=Trends.candles)
async def process_filtro(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['candles'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO")
		await Trends.next()
		await message.reply("OK\n\nPosso iniciar?",reply_markup=markup)

@dp.message_handler(state=Trends.finish)
async def process_FINSH(message: types.Message, state: FSMContext):
	global API_TOKEN
	async with state.proxy() as data:
		data['finish'] = message.text
		markup = nav.mainMenu
		if data['finish'] == "SIM":
			await bot.send_message(message.chat.id,'Ok, vou analisar pra você calma ai ja volto😜😋. se demorar mais que 1 min eu não encontrei nada, então me peça outro filtro.',parse_mode=ParseMode.HTML,reply_markup=markup)
			threading.Thread(target=controlParameter.Tendencia, args=(API,data['pair'],int(data['time']),int(data['candles']),message.chat.id,message.from_user.first_name,API_TOKEN),daemon=True).start()
		else:
				await message.reply("🦁:Ok {0}, para começar novamente cique em /TRD".format(message.from_user.first_name),reply_markup=markup)
	await state.finish()

##########NTC#################
@dp.message_handler(commands='ntc')
async def cmd_delaytss(message: types.Message):
	MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o NTC", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
	
	try:
		global API
		await message.reply('Ok, vou analisar pra você calma ai ja volto😜😋')
		threading.Thread(target=controlCatalog.checar_noticias, args=(message.chat.id,API_TOKEN),daemon=True).start()
	except: 
		await message.reply('{0} Ok, Erro'.format(message.from_user.first_name))
		pass

########CHEK################
@dp.message_handler(commands='CHK')
async def cmd_trend(message: types.Message):
	MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o CHK", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
	
	if True:
		await Check.gale.set()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add('0','1','2','cancelar')
		await message.reply("🦁:Ok {0}\n\nQuantos gales?".format(message.from_user.first_name),reply_markup=markup)
	else:
		await message.reply("🦁:{0}\n\nSó Membro".format(message.from_user.first_name)) 
		await message.reply(MENSAGE.ALL.value +"\nID:"+str(message.chat.id),parse_mode=ParseMode.HTML)
	

@dp.message_handler(lambda message: message.text not in ['0','1','2'] , state=Check.gale)
async def process_typefiltro_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido,Quantos gales?',parse_mode=ParseMode.HTML)

@dp.message_handler(state=Check.gale)
async def process_touro(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['gale'] = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add(controlParameter.dateTimeNowForString()[:11])
	await Check.next()
	await message.reply("ok\n\nQual data (dia/mês/ano).",reply_markup=markup)

@dp.message_handler(lambda message: True != controlParameter.validateD(message.text), state=Check.date)
async def process_typedate_invalid(message: types.Message):
	return await message.reply("invalido, escolha a data")
	
@dp.message_handler(state=Check.date)
async def process_optionsdate(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['date'] = message.text
	markup = nav.mainMenu

	await Check.next()
	await message.reply("Ok\n\nEnvie seus sinais Agora.",reply_markup=markup)

@dp.message_handler(lambda message: True != controlParameter.ValiList(message.text), state=Check.signals)
async def process_typedate_invalid(message: types.Message):
	check, lista, reason = controlParameter.ValidaList(message.text)
	if check:
		await bot.send_message(message.chat.id,reason,parse_mode=ParseMode.HTML)
		return await message.reply(lista)
	else:
		return await message.reply(reason)

@dp.message_handler(state=Check.signals)
async def process_signals(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['signals'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO")
		await Check.next()
		await message.reply("OK\n\nPosso iniciar?",reply_markup=markup)

@dp.message_handler(state=Check.finish)
async def process_FINSH(message: types.Message, state: FSMContext):
	global API_TOKEN
	async with state.proxy() as data:
		data['finish'] = message.text
		markup = nav.mainMenu
		if data['finish'] != "NÃO":
			await bot.send_message(message.chat.id,'Ok, vou analisar pra você calma ai ja volto😜😋. aguarde o tempo é conforme o pedido e eu ainda não sou flash😜.',parse_mode=ParseMode.HTML,reply_markup=markup)
			arqname = str(datetime.now())
			arqname = arqname.replace(".","")
			arqname = arqname.replace(" ","")
			arqname = arqname.replace(":","")
			arqname = arqname.replace("-","")
			arqname = str(message.from_user.first_name)+"#"+arqname
			threading.Thread(target=ControlCheck.check, args=(API,API_TOKEN,message.chat.id,data['signals'],data['gale'],data['date'],arqname),daemon=True).start()
		else:
			await message.reply("🦁:Ok {0}, para começar novamente cique em /CHK".format(message.from_user.first_name),reply_markup=markup)
	await state.finish()
#
#
##countlis = lista.split("\n")
##if len(countlis) <= 140:
#	#
##else:
###############CATALOOOOG####################
@dp.message_handler(commands='CTG')
async def cmd_sgale(message: types.Message):
	MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o CT SINAIS", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
	
	if True:
		await Cat.dias.set()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add('1','2','3','4','5','6','7','8','9','10','cancelar')
		await message.reply("🦁:Ok {0}\nQuantos dias?".format(message.from_user.first_name),reply_markup=markup)
	else:
		await message.reply("🦁:{0}\n\nSó Membro".format(message.from_user.first_name)) 
		await message.reply(MENSAGE.ALL.value +"\nID:"+str(message.chat.id),parse_mode=ParseMode.HTML)
	

@dp.message_handler(lambda message: message.text != is_number(message.text) , state=Cat.dias)
async def process_typefiltro_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido, Quantos dias?',parse_mode=ParseMode.HTML)

@dp.message_handler(state=Cat.dias)
async def process_touro(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['dias'] = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("0","1","2","cancelar")
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		await Cat.next()
		await message.reply("🦁:Ok\n\nQuantos gales?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["0","1","2","cancelar"], state=Cat.gale)
async def process_typeGale_invalid(message: types.Message):
	return await message.reply("Invalido, escolha gale no teclado")
@dp.message_handler(state=Cat.gale)
async def process_typeGale(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['gale'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("50","51","52","53","54","55","56","57","58","0",
		"60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99","100","cancelar")
		await Cat.next()
		await message.reply("🦁:Ok\n\nqual porcentagem minima da análise?",reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["50","51","52","53","54","55","56","57","58","0","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","cancelar"], state=Cat.analysePct)
async def process_typeanalysePct_invalid(message: types.Message):
	return await message.reply("Invalido, escolha a opção no teclado")


@dp.message_handler(state=Cat.analysePct)
async def process_analysePct(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['analysePct'] = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("ON","OFF","cancelar")
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		await Cat.next()
		await message.reply("🦁:Ok\n\nVai ativar o analizador de Tendência?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["ON","OFF","cancelar"], state=Cat.trend)
async def process_typetrend_invalid(message: types.Message):
	return await message.reply("Invalido, escolha a opção no teclado")

@dp.message_handler(state=Cat.trend)
async def process_trend(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['trend'] = message.text
	if data['trend'] == "ON":
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
		"90","91","92","93","94","95","96","97","98","99","cancelar")
		await Cat.next()
		await message.reply("🦁:OK\n\nqual media EMA para análise",reply_markup=markup)
	elif "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("0")
		await Cat.next()
		await message.reply("🦁:OK\n\nA me desculpe é mesmo! voçê não selecionou tendencia escolha essa opção ok?(0) ..",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["1","2","3","4","5","6","7","8","9",
		"10","11","12","13","14","15","16","17","18","19",
		"20","21","22","23","24","25","26","27","28","29",
		"30","31","32","33","34","35","36","37","38","39",
		"40","41","42","43","44","45","46","47","48","49",
		"50","51","52","53","54","55","56","57","58","59",
		"60","61","62","63","64","65","66","67","68","69",
		"70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99","cancelar","0"], state=Cat.trendPct)
async def process_typedate_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido, MEDIA',parse_mode=ParseMode.HTML)


@dp.message_handler(state=Cat.trendPct)
async def process_trendpct(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['trendPct'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		await Cat.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add('Todos','ABERTOS','BTCUSD','EOSUSD','ETHUSD','LTCUSD','XRPUSD','EURUSD','EURGBP','GBPJPY','EURJPY','GBPUSD','USDJPY','AUDCAD','NZDUSD','USDCHF','EURUSD-OTC','EURGBP-OTC','USDCHF-OTC','EURJPY-OTC','NZDUSD-OTC','GBPUSD-OTC','GBPJPY-OTC','USDJPY-OTC','AUDCAD-OTC','AUDUSD','USDCAD','AUDJPY','GBPCAD','GBPCHF','GBPAUD','EURCAD','CADCHF','EURAUD','EURNZD','AUDCHF','AUDNZD','CADJPY','EURCHF','GBPNZD','NZDCAD','NZDJPY','NZDCHF','cancelar')
		await message.reply("🦁:OK\n\nquais pares?\npara mais de um par espaço ex: EURUSD EURAUD",reply_markup=markup)
	
@dp.message_handler(lambda message: message.text != is_par(message.text), state=Cat.pairs)
async def process_typedate_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido, quais par?',parse_mode=ParseMode.HTML)


@dp.message_handler(state=Cat.pairs)
async def process_trendpct(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['pairs'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		await Cat.next()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("1","5","15","60","cancelar")
		await message.reply("🦁:OK\n\nqual timeframe?",reply_markup=markup)
	
@dp.message_handler(lambda message: message.text not in ["1","5","15","60"], state=Cat.time)
async def process_typedate_invalid(message: types.Message):
	await bot.send_message(message.chat.id,'Invalido,quais timeframe?',parse_mode=ParseMode.HTML)

@dp.message_handler(state=Cat.time)
async def process_trendpct(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['time'] = message.text
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add(controlParameter.dateTimeNowForString()[:11])
	await Cat.next()
	await message.reply("ok\n\n Apartir de qual data digite (dia/mês/ano).",reply_markup=markup)

@dp.message_handler(lambda message: True != controlParameter.validateD(message.text), state=Cat.date)
async def process_typedate_invalid(message: types.Message):
	return await message.reply("invalido, escolha a data")
	
@dp.message_handler(state=Cat.date)
async def process_optionsdate(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['date'] = message.text
	if "cancelar" in message.text.lower():
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("CALL","PUT","Todos")
		await Cat.next()
		await message.reply("OK\n\nqual Direção?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["CALL","PUT","Todos"], state=Cat.dir)
async def process_typedate_invalid(message: types.Message):
	return await message.reply("invalido, escolha opção do teclado")
	
@dp.message_handler(state=Cat.dir)
async def process_optionsdate(message: types.Message, state: FSMContext):
	markup = nav.mainMenu
	async with state.proxy() as data:
		data['dir'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("🦁:Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO")
		await Cat.next()
		await message.reply("OK\n\nPosso iniciar?",reply_markup=markup)

@dp.message_handler(state=Cat.finish)
async def process_FINSH(message: types.Message, state: FSMContext):
	global API_TOKEN
	async with state.proxy() as data:
		data['finish'] = message.text
		markup = nav.mainMenu
		if data['finish'] == "SIM":
			await bot.send_message(message.chat.id,'Ok, vou analisar pra você calma ai ja volto😜😋. aguarde o tempo é conforme o pedido e eu ainda não sou flash😜.',parse_mode=ParseMode.HTML,reply_markup=markup)
			arqname = str(datetime.now())
			arqname = arqname.replace(".","")
			arqname = arqname.replace(" ","")
			arqname = arqname.replace(":","")
			arqname = arqname.replace("-","")
			arqname = str(message.from_user.first_name)+"#"+arqname
			pairs = data['pairs'].split(' ')
			time = data['time'].split(' ')						
			threading.Thread(target=controlCatalog.catalog, args=(API,"vip",int(data['dias']),int(data['analysePct']),int(data['gale']),pairs,time,'OFF',data['trend'],int(data['trendPct']),arqname,str(message.chat.id),API_TOKEN,data['date'],data['dir']), daemon=True).start()
			
		else:
			await message.reply("🦁:Ok {0}, para começar novamente cique em /CTG".format(message.from_user.first_name),reply_markup=markup)
	await state.finish()
	


###########ANALY##############################33

class Prob(StatesGroup):
	pair = State()
	analysePct = State()
	time = State()
	filtro = State()
	sistema = State()
	finish = State()

@dp.message_handler(commands='catalogar')
async def cmd_catalogar(message: types.Message):
	MsgTo.send_msg(str(message.chat.username)+" - "+str(message.chat.id)+" Acessou o ATALOGAR ESTRATÉ", '1399223120','6298618464:AAE56s4jqCTmUhUs6s8On8xGkntVEAZ-rgM')
	
	if True:
		await Prob.pair.set()
		await message.reply("Ok {0}\n\nVerificando pares abertos.. aguarde".format(message.from_user.first_name))
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add('cancelar')
		markup.add('TODOS')
		s, data = connectDao.getParesBd()
		if s:
			for pars in data:
				markup.add(pars)
		await message.reply("Ok {0}\n\nEscolha uma paridade ou Todos para catalogar todas segundo os próximos filtros".format(message.from_user.first_name),reply_markup=markup)
	else:
		await message.reply("🦁:{0}\n\nSó Membro".format(message.from_user.first_name)) 
		await message.reply(MENSAGE.ALL.value +"\nID:"+str(message.chat.id),parse_mode=ParseMode.HTML)

@dp.message_handler(lambda message: message.text not in ['TODOS','EURAUD','AUDNZD','GBPNZD','USDCAD','AUDJPY','GBPCAD',"USDINR-OTC","USDSGD-OTC","USDHKD-OTC",'GBPAUD','EURUSD','EURGBP','GBPJPY','EURJPY','GBPUSD','USDJPY','AUDCAD','NZDUSD','USDCHF','AUDUSD','EOSUSD','XRPUSD','ETHUSD','LTCUSD','BTCUSD','USDJPY-OTC','AUDCAD-OTC','EURUSD-OTC','EURGBP-OTC','USDCHF-OTC','EURJPY-OTC','NZDUSD-OTC','GBPUSD-OTC','GBPJPY-OTC','EURCAD','cancelar'], state=Prob.pair)
async def process_sev_invalid(message: types.Message):
	return await message.reply("escolha a opção no teclado")


@dp.message_handler(state=Prob.pair)
async def process_pair(message: types.Message, state: FSMContext):
	markup = types.ReplyKeyboardRemove()
	async with state.proxy() as data:
		if message.text == "TODOS":
			data['pair'] = None
		else:
			data['pair'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("50","51","52","53","54","55","56","57","58","0",
		"60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99","cancelar")
		await Prob.next()
		await message.reply("Ok\n\nqual porcentagem para análise?",reply_markup=markup)
	


@dp.message_handler(lambda message: message.text not in ["50","51","52","53","54","55","56","57","58","0",
		"60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79",
		"80","81","82","83","84","85","86","87","88","89",
		"90","91","92","93","94","95","96","97","98","99","cancelar"], state=Prob.analysePct)
async def process_pair_invalid(message: types.Message):
	return await message.reply("escolha a opção no teclado")


@dp.message_handler(state=Prob.analysePct)
async def process_analysePct(message: types.Message, state: FSMContext):
	markup = types.ReplyKeyboardRemove()
	async with state.proxy() as data:
		data['analysePct'] = message.text
	if 'cancelar' == message.text.lower():
		await message.reply("Cancelado  ")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("M5","M1","cancelar")
		await Prob.next()
		await message.reply("OK\n\n Você quer analisar em que timeframe?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["M5","M1", 'cancelar'], state=Prob.time)
async def process_timecat_invalid(message: types.Message):
	return await message.reply("escolha a opção no teclado")

@dp.message_handler(state=Prob.time)
async def process_times(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['time'] = message.text
	if 'cancelar' in  message.text.lower():
		await message.reply("Cancelado  ")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("FIXA","G1","G2","cancelar")
		await Prob.next()
		await message.reply("OK\n\nDeseja filtrar a quantos gales?",reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["FIXA","G1","G2","cancelar"], state=Prob.filtro)
async def process_filtalid(message: types.Message):
	return await message.reply("escolha oção do teclado, Deseja filtrar a quantos gales?")

@dp.message_handler(state=Prob.filtro)
async def process_filtro(message: types.Message, state: FSMContext):
	global M5LI,M15LI,M1LI
	async with state.proxy() as data:
		data['filtro'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("Ok, cancelado")
		await state.finish()
	else:
		if data['time'] == 'M15':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
			await Prob.next()
			markup.add("cancelar")
			for etr in M15LI:
				markup.add(etr)
			await message.reply("OK\n\nSelecione uma estratégia..",reply_markup=markup)
		elif data['time'] == 'M5':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
			markup.add("cancelar")
			await Prob.next()
			for etr in M5LI:
				markup.add(etr)
			await message.reply("OK\n\nSelecione uma estratégia..",reply_markup=markup)

		elif data['time'] == 'M1':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
			markup.add("cancelar")
			await Prob.next()
			for etr in M1LI:
				markup.add(etr)
			await message.reply("OK\n\nSelecione uma estratégia..",reply_markup=markup)



@dp.message_handler(lambda message: message.text not in ALLLI, state=Prob.sistema)
async def process_strat_invalid(message: types.Message):
	return await message.reply("Estratégia invalida")



@dp.message_handler(state=Prob.sistema)
async def process_sistema(message: types.Message, state: FSMContext):
	markup = types.ReplyKeyboardRemove()
	async with state.proxy() as data:
		if message.text == 'TODOS':
			data['sistema'] = None
		else:
			data['sistema'] = message.text
	if "cancelar" in message.text.lower():
		await message.reply("Ok, cancelado")
		await state.finish()
	else:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
		markup.add("SIM","NÃO")
		await Prob.next()
		await message.reply("OK\n\nPosso iniciar?",reply_markup=markup)

@dp.message_handler(state=Prob.finish)
async def process_FINSH(message: types.Message, state: FSMContext):
	global API_TOKEN
	async with state.proxy() as data:
		data['finish'] = message.text
		markup = types.ReplyKeyboardRemove()
		if data['finish'] == "SIM":
			await bot.send_message(message.chat.id,'Ok, vou analisar.',parse_mode=ParseMode.HTML,reply_markup=markup)
			threading.Thread(target=controlCatalogTre.catalogAnaly, args=(API_TOKEN,message.chat.id,data['pair'],int(data['analysePct']),int(data['time'][1:]),data['filtro'],data['sistema'],'vip'),daemon=True).start()
			await state.finish()
		else:
			markup = nav.mainMenu
			await message.reply("Ok {0}, pode começar novamente ".format(message.from_user.first_name),reply_markup=markup)
	await state.finish()
@dp.message_handler()
async def bot_message(message: types.Message):
	# await bot.send_message(message.from_user.id, message.text) 
	if message.text == '📊TENDÊNCIA📊':
		await cmd_fctociclos(message)
	elif message.text == '📝CHECK LIST📝':      
		await cmd_trend(message)
	elif message.text == '📡NOTÍCIAS📡':     
		await cmd_delaytss(message)
	elif message.text == '🔰CATALOGAR SINAIS II🔰':
		await cmd_sgales(message)
	elif message.text == '🔰CATALOGAR SINAIS🔰':
		await cmd_sgale(message)
	elif message.text == '🔢CALCULADORAS🔢':  
		await cmd_gerenciamento(message)
	elif message.text == '🔣JUROS COMPOSTO🔣':
		await process_jurosc(message)
	elif message.text == 'oi':
		markup = nav.mainMenu
		await bot.send_message(message.from_user.id,'olá, esse é menu!',parse_mode=ParseMode.HTML,reply_markup=markup)

	
if __name__ == '__main__':
	#print(datetime.now())
	executor.start_polling(dp, skip_updates=False)
