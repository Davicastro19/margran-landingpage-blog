import json
import requests,sys,time
from time import sleep
from threading import Thread, Lock
from Controller.controlConfig import MsgTo
from Controller.controlConfig import controlParameter

global config
config = {'url': 'https://api.telegram.org/bot1554362014:AAEEvqGxDdp2yhqKauJ41kA65X0Z3E9jxGk/', 'lock': Lock()}

def del_update(data, telegramTk):
	Lock().acquire()
	requests.post('https://api.telegram.org/bot'+telegramTk+'/' + 'getUpdates', {'offset': data['update_id']+1})
	Lock().acquire()
def send_message(data, msg,telegramTk):
	Lock().acquire()
	requests.post('https://api.telegram.org/bot'+telegramTk+'/' + 'sendMessage', {'chat_id': data['message']['chat']['id'], 'text': str(msg)})
	Lock().acquire()
class TelegramAPis: 
	def aut(API,telegramTk,ButtonStop,ButtonStart,lableErroOperate, idd,ButtonExit,BoxAga,BoxMqui,BoxMtrin,BoxLista,BoxOtc,BoxPricAc,Mylist,PctgMins,BoxStopLoss_2,BoxStopWin_2,Pay,MysList,BoxPosDoj,BoxPrStop,comboBoxG_2,comboBoxG,MysListBox,ButtonSave_2,BoxEntrada,BoxStopLoss,BoxStopWin,BoxEntGale,doubleSpinBox_3,BoxEntrNivel,BoxFtNv,Conta):
		#try:
		if True:
			while True:
				x = ''
				while 'result' not in x:
					try:
						x = json.loads(requests.get('https://api.telegram.org/bot'+telegramTk+'/' + 'getUpdates').text)
						if x['ok'] == False:
							if 'Conflict' in x['description']:
								ButtonExit.click()
					except Exception as e:
						x = ''
						if 'Failed to establish a new connection' in str(e):
							msg='perda de conexão no telegram'
							lableErroOperate.setText(msg)
							Thread(target=send_message, args=(data, msg,telegramTk)).start()
							pass
						else:
							print(e)
							a = 'Erro TL: erro desconhecido '
							lableErroOperate.setText(a)
							pass
				if len(x['result']) > 0:
					for data in x['result']:
						Thread(target=del_update, args=(data, telegramTk )).start()
						if 'entities' in data['message']:
							if data['message']['entities'][0]['type'] == 'bot_command':
								if '/parar' in data['message']['text']:
									msg = "ok AW Bot parou"
									ButtonStop.click()
									ButtonStart.setEnabled(True)
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/iniciar' in data['message']['text']:
									ButtonStart.click()
									ButtonStart.setDisabled(True)
									msg = 'ok iniciamos'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/m15' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxMqui.setChecked(True)
									else:
										BoxMqui.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/m30' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxMtrin.setChecked(True)
									else:
										BoxMtrin.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/h1' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxAga.setChecked(True)
									else:
										BoxAga.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/price' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxPricAc.setChecked(True)
									else:
										BoxPricAc.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/lista' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxLista.setChecked(True)
									else:
										BoxLista.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/otc' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxOtc.setChecked(True)
									else:
										BoxOtc.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/mylist' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										MysList.setChecked(True)
									else:
										MysList.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/fim' in data['message']['text']:
									try:
										msg = 'ok vou fechar o aplicativo'
										Thread(target=send_message, args=(data, msg,telegramTk)).start()
										ButtonExit.click()
										time.sleep(2)
										sys.exit()
									except Exception as a:
										sys.exit()
								elif '/sala' in data['message']['text']:
									if 'H1'  in data['message']['text']:
										MysListBox.setCurrentText("H1")	
										msg	= 'Ok, Alterado'
									elif 'M30' in data['message']['text']:
										MysListBox.setCurrentText("M30")	
										msg	= 'Ok, Alterado'
									elif  'M15' in data['message']['text']:
										MysListBox.setCurrentText("M15")	
										msg	= 'Ok, Alterado'
									elif  'LI' in data['message']['text']:
										MysListBox.setCurrentText("LISTA")
										msg	= 'Ok, Alterado'	
									elif  'OTC' in data['message']['text']:
										MysListBox.setCurrentText("OTC")
										msg	= 'Ok, Alterado'	
									elif  'PA' in data['message']['text']:
										MysListBox.setCurrentText("PRICE AC")
										msg	= 'Ok, Alterado'	
									elif  'ML' in data['message']['text']:
										MysListBox.setCurrentText("MINHA LISTA")
										msg	= 'Ok, Alterado'
									else:
										msg	= 'Invalido, tente novamente'
									Thread(target=send_message, args=(data, msg, telegramTk)).start()
								elif '/save' in data['message']['text']:
									ButtonSave_2.click()
									Thread(target=send_message, args=(data, 'Salvo',telegramTk)).start()
								elif '/entrada' in data['message']['text']:
									try:
										entrada = data['message']['text'].replace("/entrada ","")
										BoxEntrada.setProperty("value", float(entrada))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/swin' in data['message']['text']:
									try:
										entrada = data['message']['text'].replace("/swin ","")
										BoxStopWin.setProperty("value", int(entrada))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/sloss' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/sloss ","")
										BoxStopLoss.setProperty("value", int(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/slossgb' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/slossgb ","")
										BoxStopLoss_2.setProperty("value", int(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/swingb' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/swingb ","")
										BoxStopWin_2.setProperty("value", int(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/payout' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/payout ","")
										Pay.setProperty("value", int(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/pcent' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/pcent ","")
										PctgMins.setProperty("value", int(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/gale' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/gale ","")
										BoxEntGale.setProperty("value", int(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/ftgale' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/ftgale ","")
										doubleSpinBox_3.setProperty("value", float(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/nivel' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/nivel ","")
										BoxEntrNivel.setProperty("value", int(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/ftnivel' in data['message']['text']:
									try:
										loss = data['message']['text'].replace("/ftnivel ","")
										BoxFtNv.setProperty("value", float(loss))
										msg = 'ok, Valor alterado'
									except:
										msg = 'Valor incorreto'
										pass
									Thread(target=send_message, args=(data, msg,telegramTk)).start()  								
								elif '/sinais' in data['message']['text']:
									lista = data['message']['text'].replace('/sinais ', '')
									check, signals, reason = controlParameter.ValidaList(lista)
									if check:
										msg = 'ok, Sinais Adicionados'
										Mylist.setText(signals)
									else:
										msg = 'ERRO: '+reason
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/pstop' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxPosDoj.setChecked(True)
									else:
										BoxPosDoj.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()
								elif '/pdoji' in data['message']['text']:
									if 'ativar' in data['message']['text']:
										msg = 'ok, Ativo'
										BoxPrStop.setChecked(True)
									else:
										BoxPrStop.setChecked(False)
										msg = 'ok, Desativado'
									Thread(target=send_message, args=(data, msg,telegramTk)).start()		
								elif '/ger' in data['message']['text']:
									if 'A'  in data['message']['text']:
										comboBoxG.setCurrentText("CONSERVADOR")
										msg	= 'Ok, Alterado'	
									elif 'C' in data['message']['text']:
										comboBoxG.setCurrentText("MODERADO")
										msg	= 'Ok, Alterado'	
									elif 'D' in data['message']['text']:
										comboBoxG.setCurrentText("ATAQUE CURTO")
										msg	= 'Ok, Alterado'	
									elif 'E' in data['message']['text']:
										comboBoxG.setCurrentText("ATAQUE PERSISTENTE")
										msg	= 'Ok, Alterado'	
									elif 'F' in data['message']['text']:
										comboBoxG.setCurrentText("SOLDADO CORAJOSO")
										msg	= 'Ok, Alterado'	
									elif 'G' in data['message']['text']:
										comboBoxG.setCurrentText("AGRESSIVO")	
										msg	= 'Ok, Alterado'
									elif 'H' in data['message']['text']:
										comboBoxG.setCurrentText("ULTRA AGRESSIVO")
										msg	= 'Ok, Alterado'
									else:
										msg	= 'Invalido, tente novamente'
									Thread(target=send_message, args=(data, msg, telegramTk)).start()
								elif '/estr' in data['message']['text']:
									if 'A'  in data['message']['text']:
										comboBoxG_2.setCurrentText("FIXA")
										msg	= 'Ok, Alterado'	
									elif 'C' in data['message']['text']:
										comboBoxG_2.setCurrentText("CICLOS")
										msg	= 'Ok, Alterado'	
									elif 'D' in data['message']['text']:
										comboBoxG_2.setCurrentText("SOROSGALE")
										msg	= 'Ok, Alterado'	
									else:
										msg	= 'Invalido, tente novamente'
									Thread(target=send_message, args=(data, msg, telegramTk)).start()
								elif '/conta' in data['message']['text']:
									if 'real'  in data['message']['text']:
										Conta.setCurrentText("REAL")
										msg	= 'Ok, Alterado para Real'	
									else:
										Conta.setCurrentText("PRATICA")
										msg	= 'Ok, Alterado para Pratica'
									Thread(target=send_message, args=(data, msg, telegramTk)).start()
								elif '/menu' in data['message']['text']:
									msg = '''
//menu   | menu
<b>Atenção nos comandos a seguir para controlar o bot via Telegram:</b>

<b>Parar o ALLWINBOT:</b>
	Comando: /parar

<b>Iniciar o ALLWINBOT:</b>
	Comando: /iniciar
	
<b>Escolher Sala para alterar gerenciamento:</b>
		Comando: /sala
		Parametro: 	'H1'  -> H1
					'M30' -> M30		
					'M15' -> M15		
					'LI'  -> LISTA		
					'OTC' -> OTC		
					'PA'  -> PRICE AC	
					'ML'  -> MINHA LISTA
		EX: /sala H1
	
<b>Escolher Estratégia de ganho:</b>
		Comando: /ger
		Parametro: 	'A' -> CONSERVADOR
					'C' -> MODERADO
					'D' -> ATAQUE CURTO
					'E' -> ATAQUE PERSISTENTE
					'F' -> SOLDADO CORAJOSO
					'G' -> AGRESSIVO	
		EX: /ger A
<b>Alterar valor da entrada(%):</b>
		Escolher Estratégia de ganho:
		Comando: /entrada
		Parametro:  numero flutuante
		EX: /entrada 2.50
	
<b>Alterar valor da stop loss(%):</b>	
		Comando: /sloss
		Parametro:  numero inteiro
		EX: /sloss 20
	
<b>Alterar valor da stop win(%):</b>	
		Comando: /swin
		Parametro:  numero inteiro
		EX: /swin 5
	
<b>Alterar valor do gale:	</b>
		Comando: /gale
		Parametro:  numero inteiro
		EX: /gale 2
	
<b>Alterar fator do gale(%):</b>	
		Comando: /ftgale
		Parametro:  numero flutuante
		EX: /ftgale 2.50
	
<b>Alterar nivel(Somente em CICLOS ou SOROSGALE):</b>	
		Comando: /nivel
		Parametro:  numero inteiro
		EX: /nivel 2
	
<b>Alterar fator do nivel(Somente em CICLOS ou SOROSGALE):</b>	
		Comando: /nivel
		Parametro:  numero flutuante
		EX: /nivel 2.60
	
<b>Ativar ou desativar Pos Doji:</b>
		Comando: /pdoji
		ATIVAR:
			Parametro: ativar  
			EX: /pdoji ativar
		DESATIVAR
			Parametro: nada  
			EX: /pdoji
	
<b>Ativar ou desativar Pre Stop:</b>
		Comando: /pstop
		ATIVAR:
			Parametro: ativar  
			EX: /pstop ativar
		DESATIVAR
			Parametro: nada  
			EX: /pstop

<b>Ativar ou desativar Pre Stop:</b>
		Comando: /pstop
		ATIVAR:
			Parametro: ativar  
			EX: /pstop ativar
		DESATIVAR
			Parametro: nada  
			EX: /pstop

<b>Alterar stopwin global:	</b>
		Comando: /swingb
		Parametro:  numero inteiro
		EX: /swingb 25
	
<b>Alterar stoploss global:	</b>
		Comando: /slossgb
		Parametro:  numero inteiro
		EX: /slossgb 10
	
<b>Alterar Payout min:	</b>
		Comando: /payout
		Parametro:  numero inteiro
		EX: /payout 88
	
<b>Alterar porcentagem minima:	</b>
		Comando: /pcent
		Parametro:  numero inteiro
		EX: /pcent 88
	
<b>Ativar ou desativar sala M15:</b>
		Comando: /m15
		ATIVAR:
			Parametro: ativar  
			EX: /m15 ativar
		DESATIVAR
			Parametro: nada  
			EX: /m15
		
<b>Ativar ou desativar sala M30:</b>
		Comando: /M30
		ATIVAR:
			Parametro: ativar  
			EX: /M30 ativar
		DESATIVAR
			Parametro: nada  
			EX: /M30

<b>Ativar ou desativar sala H1:</b>
		Comando: /h1
		ATIVAR:
			Parametro: ativar  
			EX: /h1 ativar
		DESATIVAR
			Parametro: nada  
			EX: /h1
		
<b>Ativar ou desativar sala PRICE ACTION:</b>
		Comando: /price
		ATIVAR:
			Parametro: ativar  
			EX: /price ativar
		DESATIVAR
			Parametro: nada  
			EX: /price

<b>Ativar ou desativar sala LISTA:</b>
		Comando: /lista
		ATIVAR:
			Parametro: ativar  
			EX: /lista ativar
		DESATIVAR
			Parametro: nada  
			EX: /lista

<b>Ativar ou desativar sala OTC:</b>
		Comando: /otc
		ATIVAR:
			Parametro: ativar  
			EX: /otc ativar
		DESATIVAR
			Parametro: nada  
			EX: /otc

<b>Ativar ou desativar MINHA LISTA:</b>
		Comando: /mylist
		ATIVAR:
			Parametro: ativar  
			EX: /mylist ativar
		DESATIVAR
			Parametro: nada  
			EX: /mylist

<b>ALterar Lista ou adicionar lista:</b>
		Comando: /sinais
		Parametro: lista  
		EX: /sinais M1;EURJPY;23:27:00;CALL
M1;EURJPY;23:31:00;PUT
M1;EURJPY;23:34:00;PUT

<b>Conta Real ou Pratica:</b>
		Comando: /conta
		REAL:
			Parametro: real  
			EX: /conta real
		PRATICA:
			Parametro: nada  
			EX: /conta
										'''
									Thread(target=MsgTo.send_msg, args=(msg, idd, telegramTk,lableErroOperate)).start()
								elif '/start' in data['message']['text']:
									msg = '''
/menu   | menu
<b>Atenção nos comandos a seguir para controlar o bot via Telegram:</b>

<b>Parar o ALLWINBOT:</b>
	Comando: /parar

<b>Iniciar o ALLWINBOT:</b>
	Comando: /iniciar
	
<b>Escolher Sala para alterar gerenciamento:</b>
		Comando: /sala
		Parametro: 	'H1'  -> H1
					'M30' -> M30		
					'M15' -> M15		
					'LI'  -> LISTA		
					'OTC' -> OTC		
					'PA'  -> PRICE AC	
					'ML'  -> MINHA LISTA
		EX: /sala H1
	
<b>Escolher Estratégia de ganho:</b>
		Comando: /ger
		Parametro: 	'A' -> FIXA
					'C' -> CICLOS
					'D' -> SOROSGALE
					'E' -> GALE

<b>Escolher Gerenciamento:</b>
		Comando: /ger
		Parametro: 	'A' -> CONSERVADOR
					'C' -> MODERADO
					'D' -> ATAQUE CURTO
					'E' -> ATAQUE PERSISTENTE
					'F' -> SOLDADO CORAJOSO
					'G' -> AGRESSIVO	
		EX: /ger A
<b>Alterar valor da entrada(%):</b>
		Escolher Estratégia de ganho:
		Comando: /entrada
		Parametro:  numero flutuante
		EX: /entrada 2.50
		
<b>Alterar valor da stop loss(%):</b>	
		Comando: /sloss
		Parametro:  numero inteiro
		EX: /sloss 20
	
<b>Alterar valor da stop win(%):</b>	
		Comando: /swin
		Parametro:  numero inteiro
		EX: /swin 5
	
<b>Alterar valor do gale:	</b>
		Comando: /gale
		Parametro:  numero inteiro
		EX: /gale 2
	
<b>Alterar fator do gale(%):</b>	
		Comando: /ftgale
		Parametro:  numero flutuante
		EX: /ftgale 2.50
	
<b>Alterar nivel(Somente em CICLOS ou SOROSGALE):</b>	
		Comando: /nivel
		Parametro:  numero inteiro
		EX: /nivel 2
	
<b>Alterar fator do nivel(Somente em CICLOS ou SOROSGALE):</b>	
		Comando: /nivel
		Parametro:  numero flutuante
		EX: /nivel 2.60
	
<b>Ativar ou desativar Pos Doji:</b>
		Comando: /pdoji
		ATIVAR:
			Parametro: ativar  
			EX: /pdoji ativar
		DESATIVAR
			Parametro: nada  
			EX: /pdoji
	
<b>Ativar ou desativar Pre Stop:</b>
		Comando: /pstop
		ATIVAR:
			Parametro: ativar  
			EX: /pstop ativar
		DESATIVAR
			Parametro: nada  
			EX: /pstop

<b>Ativar ou desativar Pre Stop:</b>
		Comando: /pstop
		ATIVAR:
			Parametro: ativar  
			EX: /pstop ativar
		DESATIVAR
			Parametro: nada  
			EX: /pstop

<b>Alterar stopwin global:	</b>
		Comando: /swingb
		Parametro:  numero inteiro
		EX: /swingb 25
	
<b>Alterar stoploss global:	</b>
		Comando: /slossgb
		Parametro:  numero inteiro
		EX: /slossgb 10
	
<b>Alterar Payout min:	</b>
		Comando: /payout
		Parametro:  numero inteiro
		EX: /payout 88
	
<b>Alterar porcentagem minima:	</b>
		Comando: /pcent
		Parametro:  numero inteiro
		EX: /pcent 88
	
<b>Ativar ou desativar sala M15:</b>
		Comando: /m15
		ATIVAR:
			Parametro: ativar  
			EX: /m15 ativar
		DESATIVAR
			Parametro: nada  
			EX: /m15
		
<b>Ativar ou desativar sala M30:</b>
		Comando: /M30
		ATIVAR:
			Parametro: ativar  
			EX: /M30 ativar
		DESATIVAR
			Parametro: nada  
			EX: /M30

<b>Ativar ou desativar sala H1:</b>
		Comando: /h1
		ATIVAR:
			Parametro: ativar  
			EX: /h1 ativar
		DESATIVAR
			Parametro: nada  
			EX: /h1
		
<b>Ativar ou desativar sala PRICE ACTION:</b>
		Comando: /price
		ATIVAR:
			Parametro: ativar  
			EX: /price ativar
		DESATIVAR
			Parametro: nada  
			EX: /price

<b>Ativar ou desativar sala LISTA:</b>
		Comando: /lista
		ATIVAR:
			Parametro: ativar  
			EX: /lista ativar
		DESATIVAR
			Parametro: nada  
			EX: /lista

<b>Ativar ou desativar sala OTC:</b>
		Comando: /otc
		ATIVAR:
			Parametro: ativar  
			EX: /otc ativar
		DESATIVAR
			Parametro: nada  
			EX: /otc

<b>Ativar ou desativar MINHA LISTA:</b>
		Comando: /mylist
		ATIVAR:
			Parametro: ativar  
			EX: /mylist ativar
		DESATIVAR
			Parametro: nada  
			EX: /mylist
<b>ALterar Lista ou adicionar lista:</b>
		Comando: /sinais
		Parametro: lista  
		EX: /sinais M1;EURJPY;23:27:00;CALL
M1;EURJPY;23:31:00;PUT
M1;EURJPY;23:34:00;PUT

<b>Conta Real ou Pratica:</b>
		Comando: /conta
		REAL:
			Parametro: real  
			EX: /conta real
		PRATICA:
			Parametro: nada  
			EX: /conta
										'''
									Thread(target=MsgTo.send_msg, args=(msg, idd, telegramTk,lableErroOperate)).start()
						else:
							if data['message']['text'] == 'oi':
								Thread(target=send_message, args=(data, 'Olá, tudo bem?', telegramTk)).start()
					sleep(4)	
		#except Exception as a:
		#	MsgTo.send_msg(str(a)+str(idd), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0',lableErroOperate)
		#	pass