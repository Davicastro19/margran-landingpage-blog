from datetime import datetime, timedelta
from time import sleep, time
from Controller.cantrolDate import tnumericos,dateTimeNowFordate,dateTimeNowForString
import json,re,requests
import pandas as pd
import numpy as np
from telegram import ParseMode
from bs4 import BeautifulSoup
import os
import telegram
import json
from iqoptionapi.constants import ACTIVCATALAGVn, ACTIVCATALAGVip,pares
import requests,logging
from time import sleep
from threading import Lock
logger = logging.getLogger()
logger.disabled = True

class MsgTo:
	def upload_file(file,idd,API_TOKEN):
		config = {'url': 'https://api.telegram.org/bot'+API_TOKEN+'/', 'lock': Lock(), 'url_file': 'https://api.telegram.org/file/bot'+API_TOKEN+'/'}
	
		formatos = {'png': {'metodo': 'sendPhoto', 'send': 'photo'},
					'text': {'metodo': 'sendDocument', 'send': 'document'},
					 'pdf': {'metodo': 'sendDocument', 'send': 'document'}}
		return requests.post(config['url'] + formatos['text' if '.txt' in file else 'png']['metodo'], {'chat_id': idd}, files={formatos['text' if '.txt' in file else 'png']['send']: open(file, 'rb')}).text

	def send_msg(texto,idd,API_TOKEN):
		bot = telegram.Bot(token=''+API_TOKEN+'')
		bot.sendMessage(parse_mode=ParseMode.HTML, chat_id=idd, text=texto)


class controlCatalog:
	def getal_pares(API):
		conf = {'pares':[]}
		P = ''
		while 1:
			P = API.get_all_open_time()
			if P != '':
				break
		if P != '':
			for p in P['digital']:
				if P['digital'][p]['open']:
					if p not in conf['pares']:
						#dash(' ' + cr('*', 'y') + ' Capturando paridades.. ' + cr(p, 'y') + '(' + str(len(conf['pares'])) + ')')
						sleep(0.1)
						conf['pares'].append(p)
			for p in P['turbo']:
				if P['turbo'][p]['open']:
					if p not in conf['pares']:
					# dash(' ' + cr('*', 'y') + ' Capturando paridades.. ' + cr(p, 'y') + '(' + str(len(conf['pares'])) + ')')
						sleep(0.1)
						conf['pares'].append(p)
			for p in P['binary']:
				if P['binary'][p]['open']:
					if p not in conf['pares']:
						#dash(' ' + cr('*', 'y') + ' Capturando paridades.. ' + cr(p, 'y') + '(' + str(len(conf['pares'])) + ')')
						sleep(0.1)
						conf['pares'].append(p)
			del P
		return conf
	def get_pares(API,timeF,pairs):
		pair = []
		P = ''
		t = 0	
		while True:
			try:
				P = API.get_all_open_time()
			except:
				pass	
			
			if P != '' or t == 5 : break
			t += 1

		if P != '' and type(P) != None:
			for p in P['digital']:

				if P['digital'][p]['open']: 
					last_payout = pares['pares']['digital'][p] if p in pares['pares']['digital'] else 0
					pares['pares']['digital'].update({p: last_payout})

				elif  P['digital'][p]['open'] == False and p in pares['pares']['digital']:
					del pares['pares']['digital'][p]

			d = API.get_all_profit()

			for p in P['turbo']: 
				if P['turbo'][p]['open']: 
					try:
						pares['pares']['turbo'].update({p: d[p]['turbo']})
						sleep(0.1)
					except:
						pass

				elif P['turbo'][p]['open'] == False and p in pares['pares']['turbo']:
						del pares['pares']['turbo'][p]

			for p in P['binary']:
				if P['binary'][p]['open']:  
					try:
						pares['pares']['binary'].update({p: d[p]['binary']})
						sleep(0.1)
					except:
						pass

				elif P['binary'][p]['open'] == False and p in pares['pares']['binary']:
					del pares['pares']['binary'][p]

			for p in pares['pares']['digital']:
				par = p
				API.subscribe_strike_list(par,timeF)
				timer = 0

				while True:
					d = ''
					d = API.get_digital_current_profit(par,timeF)
					if d != False:
						pares['pares']['digital'].update({par: round((int(d) / 100), 2)})
						break
					if timer == 5:
						pares['pares']['digital'].update({par: round((int(d) / 100), 2)})
						break
					sleep(1)
					timer += 1
				API.unsubscribe_strike_list(par, timeF)

			del P
			del d

		
		for par in pares['pares']['binary']:
			if par not in pair and par in ACTIVCATALAGVip:
				pair.append(par)
		for par in pares['pares']['turbo']:
			if par not in pair and par in ACTIVCATALAGVip:
				pair.append(par)	
		for par in pares['pares']['digital']:
			if par not in pair and par in ACTIVCATALAGVip:
				pair.append(par)	
		if pairs != None:
			if pairs in pair:
				pair.clear()
				pair.append(pairs)
			else:
				pair.append("TODOS")
		return pair
	def catalogAnaly(API,telegramTk,idd,pair,analysePct,timeF,filtro,sistema):
		def catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares):
			for i in range(5):
				
				oi = dateTimeNowFordate() - timedelta(minutes=1*i)
				
				minutos = float(((oi).strftime('%M'))[1:])
				if timeF == 1:
					entrar = True if (minutos ==3 ) or (minutos == 8 ) else False
				else:
					entrar = True if (minutos ==5 ) or (minutos == 0 ) else False
				if entrar:
					horario_operacao = str(oi)[:26]
					break

			hora_teste = datetime.strptime(horario_operacao,'%Y-%m-%d %H:%M:%S.%f')
			while True:	
				entrar = True 
				resultado = []
				if entrar:
					for par in pares:
						proceed = True
						if proceed:
							for i in range(24):
								horario = hora_teste - timedelta(minutes=5*i) - timedelta(minutes=1) 
								hora_hora = horario.strftime('%Y-%m-%d %H:%M')
								ha = datetime.strptime(hora_hora,'%Y-%m-%d %H:%M')
								ha = ha + timedelta(hours=3)
								hora_analise = datetime.timestamp(ha)
								vela = API.get_candles(par,(int(timeF) * 60),6,hora_analise)
								vela[0] = 'g' if vela[0]['open'] < vela[0]['close'] else 'r' if vela[0]['open'] > vela[0]['close'] else 'd'
								vela[1] = 'g' if vela[1]['open'] < vela[1]['close'] else 'r' if vela[1]['open'] > vela[1]['close'] else 'd'
								vela[2] = 'g' if vela[2]['open'] < vela[2]['close'] else 'r' if vela[2]['open'] > vela[2]['close'] else 'd'
								cor_entrada = vela[0] + ' ' + vela[1] + ' ' + vela[2]
								if cor_entrada.count('g') > cor_entrada.count('r') : dir = 'CALL'
								if cor_entrada.count('r') > cor_entrada.count('g') : dir = 'PUT'
								if cor_entrada.count('r') == cor_entrada.count('g') and cor_entrada.count('d') > 0 : dir = False
								if dir:
									if dir == 'CALL' and vela[3]['open'] < vela[3]['close'] or dir == 'PUT' and vela[3]['open'] > vela[3]['close']:
										resultado.append('WIN')
									elif dir == 'CALL' and vela[4]['open'] < vela[4]['close'] or dir == 'PUT' and vela[4]['open'] > vela[4]['close']:
										resultado.append('WIN 1 Gale')
									elif dir == 'CALL' and vela[5]['open'] < vela[5]['close'] or dir == 'PUT' and vela[5]['open'] > vela[5]['close']:
										resultado.append('WIN 2 Gale')
									else:
										resultado.append('LOSS')
									cor_entrada = ''
						
							a= '🔰🔰TRÊS MOSQUETEIROS ÚLTIMAS 2 HORAS🔰🔰\n'
							a+='💹: '+str(par)+'\n'
							a+='🟢: '+str(resultado.count('WIN'))+'\n'
							a+='🟢🐔:'+str(resultado.count('WIN 1 Gale'))+'\n'
							a+='🟢🐔🐔:'+str(resultado.count('WIN 2 Gale'))+'\n'
							a+='🔴:'+str(resultado.count('LOSS'))+'\n'
							soma_total = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale') + resultado.count('LOSS')
							if filtro == 'FIXA':
								soma_win = resultado.count('WIN')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🦁: '+str(res)
							elif filtro == 'G1':
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🐔: '+str(res)
							elif filtro == 'G2':
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🐔🐔: '+str(res)
							else:
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
							resultado = []
							if int((soma_win/soma_total)*100) >= analysePct:
								MsgTo.send_msg(a,idd,telegramTk)
								if pair != None:
									return pair
								
					break
			return pair
		
		def catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares):
			for i in range(5):
				oi = dateTimeNowFordate() - timedelta(minutes=1*i)
				minutos = float(((oi).strftime('%M'))[1:])
				if int(timeF) == 1:
					entrar = True if (minutos ==3 ) or (minutos == 8 ) else False
				else:
					entrar = True if (minutos ==5 ) or (minutos == 0 ) else False
				if entrar:
					horario_operacao = str(oi)[:26]
					break
					
					
			hora_teste = datetime.strptime(horario_operacao,'%Y-%m-%d %H:%M:%S.%f')
			while True:
				try:
					entrar = True 
					resultado = []
					if entrar:
						for par in pares:
							proceed = True
							if proceed:
								for i in range(24):
									horario = hora_teste - timedelta(minutes=5*i) - timedelta(minutes=1) 
									hora_hora = horario.strftime('%Y-%m-%d %H:%M')
									ha = datetime.strptime(hora_hora,'%Y-%m-%d %H:%M')
									ha = ha + timedelta(hours=3)
									hora_analise = datetime.timestamp(ha)
									vela = API.get_candles(par,(int(timeF) * 60),6,hora_analise)
									vela[0] = 'g' if vela[0]['open'] < vela[0]['close'] else 'r' if vela[0]['open'] > vela[0]['close'] else 'd'
									vela[1] = 'g' if vela[1]['open'] < vela[1]['close'] else 'r' if vela[1]['open'] > vela[1]['close'] else 'd'
									vela[2] = 'g' if vela[2]['open'] < vela[2]['close'] else 'r' if vela[2]['open'] > vela[2]['close'] else 'd'
									cor_entrada = vela[0] + ' ' + vela[1] + ' ' + vela[2]
									if cor_entrada.count('r') == cor_entrada.count('g') and cor_entrada.count('d') > 0 : dir = False
									if cor_entrada.count('g') > cor_entrada.count('r') : dir = 'PUT'
									if cor_entrada.count('r') > cor_entrada.count('g') : dir = 'CALL'
									if dir:
									
										if dir == 'CALL' and vela[3]['open'] < vela[3]['close'] or dir == 'PUT' and vela[3]['open'] > vela[3]['close']:
											resultado.append('WIN')
										elif dir == 'CALL' and vela[4]['open'] < vela[4]['close'] or dir == 'PUT' and vela[4]['open'] > vela[4]['close']:
											resultado.append('WIN 1 Gale')
										elif dir == 'CALL' and vela[5]['open'] < vela[5]['close'] or dir == 'PUT' and vela[5]['open'] > vela[5]['close']:
											resultado.append('WIN 2 Gale')
										else:
											resultado.append('LOSS')
										cor_entrada = ''
								a= '🔰🔰MHI MINORIA ÚLTIMAS 2 HORAS🔰🔰\n'
								a+='💹: '+str(par)+'\n'
								a+='🟢: '+str(resultado.count('WIN'))+'\n'
								a+='🟢🐔:'+str(resultado.count('WIN 1 Gale'))+'\n'
								a+='🟢🐔🐔:'+str(resultado.count('WIN 2 Gale'))+'\n'
								a+='🔴:'+str(resultado.count('LOSS'))+'\n'
								soma_total = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale') + resultado.count('LOSS')
								if filtro == 'FIXA':
									soma_win = resultado.count('WIN')
									res = int((soma_win/soma_total)*100)
									if  res < 70:
										res= "🟥"+str(res)+"%🟥"
									elif res >= 70 and res <= 79:
										res= "🟧"+str(res)+"%🟧"
									elif res >= 80:
										res= "🟩"+str(res)+"%🟩"
									a+='ASSERTIVIDADE 🦁: '+str(res)
								elif filtro == 'G1':
									soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale')
									res = int((soma_win/soma_total)*100)
									if  res < 70:
										res= "🟥"+str(res)+"%🟥"
									elif res >= 70 and res <= 79:
										res= "🟧"+str(res)+"%🟧"
									elif res >= 80:
										res= "🟩"+str(res)+"%🟩"
									a+='ASSERTIVIDADE 🐔: '+str(res)
								elif filtro == 'G2':
									soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
									res = int((soma_win/soma_total)*100)
									if  res < 70:
										res= "🟥"+str(res)+"%🟥"
									elif res >= 70 and res <= 79:
										res= "🟧"+str(res)+"%🟧"
									elif res >= 80:
										res= "🟩"+str(res)+"%🟩"
									a+='ASSERTIVIDADE 🐔🐔: '+str(res)
								else:
									soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
								resultado = []
								if int((soma_win/soma_total)*100) >= analysePct:
									MsgTo.send_msg(a,idd,telegramTk)
									if pair != None:
										return pair
						break
				except Exception as a:
					print(a)
					break
			return pair		
		
		def catalogacao_tres_mosqueteiros(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares):
			for i in range(5):
				oi = dateTimeNowFordate() - timedelta(minutes=1*i)
				minutos = float(((oi).strftime('%M'))[1:])
				if int(timeF) == 1:
					entrar = True if (minutos ==1 ) or (minutos == 6 ) else False
				else:
					entrar = True if (minutos ==5 ) or (minutos == 0 ) else False
				if entrar:
					horario_operacao = str(oi)[:26]
					break


			hora_teste = datetime.strptime(horario_operacao,'%Y-%m-%d %H:%M:%S.%f')

			while True:
				entrar = True 
				resultado = []
				if entrar:
					for par in pares:
						proceed = True
						if proceed:
							for i in range(24):
								horario = hora_teste - timedelta(minutes=5*i) - timedelta(minutes=1) 
								hora_hora = horario.strftime('%Y-%m-%d %H:%M')
								ha = datetime.strptime(hora_hora,'%Y-%m-%d %H:%M')
								ha = ha + timedelta(hours=3)
								hora_analise = datetime.timestamp(ha)
								vela = API.get_candles(par,(int(timeF) * 60),4,hora_analise)
								vela[0] = 'g' if vela[0]['open'] < vela[0]['close'] else 'r' if vela[0]['open'] > vela[0]['close'] else 'd'
								if vela[0] == 'g' : dir = 'CALL'
								if vela[0] == 'r' : dir = 'PUT'
								if vela[0] == 'd' : dir = False
								if dir:
									if dir == 'CALL' and vela[1]['open'] < vela[1]['close'] or dir == 'PUT' and vela[1]['open'] > vela[1]['close']:
										resultado.append('WIN')
									elif dir == 'CALL' and vela[2]['open'] < vela[2]['close'] or dir == 'PUT' and vela[2]['open'] > vela[2]['close']:
										resultado.append('WIN 1 Gale')
									elif dir == 'CALL' and vela[3]['open'] < vela[3]['close'] or dir == 'PUT' and vela[3]['open'] > vela[3]['close']:
										resultado.append('WIN 2 Gale')
									else:
										resultado.append('LOSS')
									cor_entrada = ''
									
							a= '🔰🔰3 MOSQUETEIROS ÚLTIMAS 2 HORAS🔰🔰\n'
							a+='💹: '+str(par)+'\n'
							a+='🟢: '+str(resultado.count('WIN'))+'\n'
							a+='🟢🐔:'+str(resultado.count('WIN 1 Gale'))+'\n'
							a+='🟢🐔🐔:'+str(resultado.count('WIN 2 Gale'))+'\n'
							a+='🔴:'+str(resultado.count('LOSS'))+'\n'
							soma_total = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale') + resultado.count('LOSS')
							if filtro == 'FIXA':
								soma_win = resultado.count('WIN')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🦁: '+str(res)
							elif filtro == 'G1':
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🐔: '+str(res)
							elif filtro == 'G2':
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🐔🐔: '+str(res)
							else:
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
							resultado = []
							if int((soma_win/soma_total)*100) >= analysePct:
								MsgTo.send_msg(a,idd,telegramTk)
								if pair != None:
									return pair

					break
			return pair
		
		def catalogacao_torres_gemeas(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares):

			for i in range(5):
				oi = dateTimeNowFordate() - timedelta(minutes=1*i)
				minutos = float(((oi).strftime('%M'))[1:])
				if int(timeF) == 1:
					entrar = True if (minutos ==2 ) or (minutos == 7 ) else False
				else:
					entrar = True if (minutos ==5 ) or (minutos == 0 ) else False
				if entrar:
					horario_operacao = str(oi)[:26]
					break


			hora_teste = datetime.strptime(horario_operacao,'%Y-%m-%d %H:%M:%S.%f')

			while True:

				entrar = True 

				resultado = []

				if entrar:
					for par in pares:
						proceed = True
						if proceed:
							for i in range(24):
								horario = hora_teste - timedelta(minutes=5*i) - timedelta(minutes=int(timeF)) 
								hora_hora = horario.strftime('%Y-%m-%d %H:%M')
								ha = datetime.strptime(hora_hora,'%Y-%m-%d %H:%M')
								ha = ha + timedelta(hours=3)
								hora_analise = datetime.timestamp(ha)
								if int(timeF) == 5:
									vela = API.get_candles(par,(int(timeF) * 60),8,hora_analise)
								else:
									vela = API.get_candles(par,(int(timeF) * 60),7,hora_analise)
								vela[0] = 'g' if vela[0]['open'] < vela[0]['close'] else 'r' if vela[0]['open'] > vela[0]['close'] else 'd'
								if vela[0] == 'g' : dir = 'CALL'
								if vela[0] == 'r' : dir = 'PUT'
								if vela[0] == 'd' : dir = False
								if dir:
									if int(timeF) == 5:
										if dir == 'CALL' and vela[5]['open'] < vela[5]['close'] or dir == 'PUT' and vela[5]['open'] > vela[5]['close']:
											resultado.append('WIN')
										elif dir == 'CALL' and vela[6]['open'] < vela[6]['close'] or dir == 'PUT' and vela[6]['open'] > vela[6]['close']:
											resultado.append('WIN 1 Gale')
										elif dir == 'CALL' and vela[7]['open'] < vela[7]['close'] or dir == 'PUT' and vela[7]['open'] > vela[7]['close']:
											resultado.append('WIN 2 Gale')
										else:
											resultado.append('LOSS')
									else:
										if dir == 'CALL' and vela[4]['open'] < vela[4]['close'] or dir == 'PUT' and vela[4]['open'] > vela[4]['close']:
											resultado.append('WIN')
										elif dir == 'CALL' and vela[5]['open'] < vela[5]['close'] or dir == 'PUT' and vela[5]['open'] > vela[5]['close']:
											resultado.append('WIN 1 Gale')
										elif dir == 'CALL' and vela[6]['open'] < vela[6]['close'] or dir == 'PUT' and vela[6]['open'] > vela[6]['close']:
											resultado.append('WIN 2 Gale')
										else:
											resultado.append('LOSS')
									cor_entrada = ''
							a= '🔰🔰TORRES GEMEAS ÚLTIMAS 2 HORAS🔰🔰\n'
							a+='💹: '+str(par)+'\n'
							a+='🟢: '+str(resultado.count('WIN'))+'\n'
							a+='🟢🐔:'+str(resultado.count('WIN 1 Gale'))+'\n'
							a+='🟢🐔🐔:'+str(resultado.count('WIN 2 Gale'))+'\n'
							a+='🔴:'+str(resultado.count('LOSS'))+'\n'
							soma_total = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale') + resultado.count('LOSS')
							if filtro == 'FIXA':
								soma_win = resultado.count('WIN')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🦁: '+str(res)
							elif filtro == 'G1':
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🐔: '+str(res)
							elif filtro == 'G2':
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
								res = int((soma_win/soma_total)*100)
								if  res < 70:
									res= "🟥"+str(res)+"%🟥"
								elif res >= 70 and res <= 79:
									res= "🟧"+str(res)+"%🟧"
								elif res >= 80:
									res= "🟩"+str(res)+"%🟩"
								a+='ASSERTIVIDADE 🐔🐔: '+str(res)
							else:
								soma_win = resultado.count('WIN') + resultado.count('WIN 1 Gale') + resultado.count('WIN 2 Gale')
							resultado = []
							if int((soma_win/soma_total)*100) >= analysePct:
								MsgTo.send_msg(a,idd,telegramTk)
								if pair != None:
									return pair
					break
			return pair
		pares = controlCatalog.get_pares(API,int(timeF),pair)
		if sistema == None:
			catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
			catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
			catalogacao_tres_mosqueteiros(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
			catalogacao_torres_gemeas(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif 'MHI-MINORIA' in sistema and "TODOS" not in pares:
			catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif "MHI-MAIORIA" in sistema and "TODOS" not in pares:
			catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif "TORRES G." in sistema and "TODOS" not in pares:
			catalogacao_torres_gemeas(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif "TRÊS-MOS" in sistema and "TODOS" not in pares:
			catalogacao_tres_mosqueteiros(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif 'MHI-MINORIA' in sistema and pair == None:
			catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif "MHI-MAIORIA" in sistema and pair == None:
			catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif "TORRES G." in sistema and pair == None:
			catalogacao_torres_gemeas(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
		elif "TRÊS-MOS" in sistema and pair == None:
			catalogacao_tres_mosqueteiros(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares)
	
	def catalogAnalOcatalg(telegramTk,idd,pair,analysePct,time,filtro,quadrantes,sistema):
		if "Seven" in sistema:
			sistema = sistema.replace('Flip', 'Wick')
		# 	Todos/M5/Todas/24/G1
		if filtro == 'FIXA':
			filtro = 'G0'
		response = requests.get("https://backend.ocatalogador.com/api/v1/catalogue/{0}/{1}/{2}/{3}/{4}".format(pair,"M"+time,sistema,quadrantes,filtro))
        # Return False if can't get data
		if response.status_code != 200:
			pass
		else:
			result = json.loads(response.text)
			for cataloger in result:
				text = ''
				if cataloger['win'] > float(analysePct):
					if len(cataloger['estrategia']) <= 4: 
						text += '💠💠💠💠'+cataloger['estrategia']+'💠💠💠💠\n\n             💹'+cataloger['par']+'💹\n\n'
					elif len(cataloger['estrategia']) <=13:
						text += '💠💠💠'+cataloger['estrategia']+'💠💠💠\n\n         💹'+cataloger['par']+'💹\n\n'
					else:
						text += '💠💠'+cataloger['estrategia']+'💠💠\n\n      💹'+cataloger['par']+'💹\n\n'
					if  cataloger['win'] < float(70):
						res= "🔴"+str(cataloger['win'])+"%🔴"
					elif cataloger['win'] >= float(70) and cataloger['win'] <= float(79):
						res= "🟡"+str(cataloger['win'])+"%🟡"
					elif cataloger['win'] >= float(80):
						res= "🟢"+str(cataloger['win'])+"%🟢"
					text += '      ⏱M'+time+'⏱'+res+'\n\n'
					vels = ''
					ctt = 0
					for vel in cataloger['quadrantes']:
						if ctt ==6:
							vels += '\n'  
							ctt = 1
						else:
							ctt +=1
						if 'W' == vel:
							vels+='🟩'
						elif 'G1' == vel:
							vels+='🟨'
						elif 'G2' == vel:
							vels+='🟧'
						elif 'G3' == vel:
							vels+='🟪'
						elif 'G4' == vel:
							vels+='🟦'
						elif 'G5' == vel:
							vels+='⬛️'
						elif 'D' == vel:
							vels+='⬜️'
						elif 'H' == vel:
							vels+='🟥'
					text += vels+'\n\n'
					#text += Próxima Entrada: 19:10
					text += 'Último Quadrante: '+cataloger['ultimoQuadrante']+'\n\n'
					if filtro == 'G0':
						text += '🟩:'+str(vels.count('🟩'))+'\n'
					elif filtro == 'G1':
						text += '🟩:'+str(vels.count('🟩'))+'\n'
						text += '🟨:'+str(vels.count('🟨'))+'\n'
					elif filtro == 'G2':
						text += '🟩:'+str(vels.count('🟩'))+'\n'
						text += '🟨:'+str(vels.count('🟨'))+'\n'
						text += '🟧:'+str(vels.count('🟧'))+'\n'
					elif filtro == 'G3':
						text += '🟩:'+str(vels.count('🟩'))+'\n'
						text += '🟨:'+str(vels.count('🟨'))+'\n'
						text += '🟧:'+str(vels.count('🟧'))+'\n'
						text += '🟪:'+str(vels.count('🟪'))+'\n'
					elif filtro == 'G4':
						text += '🟩:'+str(vels.count('🟩'))+'\n'
						text += '🟨:'+str(vels.count('🟨'))+'\n'
						text += '🟧:'+str(vels.count('🟧'))+'\n'
						text += '🟪:'+str(vels.count('🟪'))+'\n'
						text += '🟦:'+str(vels.count('🟦'))+'\n'
					elif filtro == 'G5':
						text += '🟩:'+str(vels.count('🟩'))+'\n'
						text += '🟨:'+str(vels.count('🟨'))+'\n'
						text += '🟧:'+str(vels.count('🟧'))+'\n'
						text += '🟪:'+str(vels.count('🟪'))+'\n'
						text += '🟦:'+str(vels.count('🟦'))+'\n'
						text += '⬛️:'+str(vels.count('⬛️'))+'\n'
					text += 'DOJI⬜️:'+str(vels.count('⬜️'))+'\n'
					text += 'HITS🟥:'+str(vels.count('🟥'))+'\n\n\n'
					text += 'DEV: @SrDevTrader'
					
					MsgTo.send_msg(text,idd,telegramTk)
			MsgTo.send_msg("CATALOÇÃO FINALIZADA!",idd,telegramTk)
	def checar_noticias(idd,token):
		headers = requests.utils.default_headers()
		headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'})

		html = requests.get('http://br.investing.com/economic-calendar/', headers=headers)
		msg = '📊🧾💹📡NOTICIAS📡💹🧾📊\n\n'
		impacto_minimo = []
		if html.status_code == requests.codes.ok:
			html_source = BeautifulSoup(html.text, 'html.parser')
			html_body = ((html_source.find('table', {'id': 'economicCalendarData'})).find('tbody')).findAll('tr', {'class': 'js-event-item'})

			for table in html_body:
				ativo = (table.find('td', {'class': 'left flagCur noWrap'})).text.strip()
				notc = (table.find('td', {'class': 'left event'})).text.strip()
				ativo_impacto = str((table.find('td', {'class': 'sentiment'})).get('data-img_key')).replace('bull', '')
				ativo_datetime = str(table.get('data-event-datetime'))
				touro = '🐮' * int(ativo_impacto)
				if ativo in ACTIVCATALAGVn:
					msg += "💹"+str(ativo)+" | "+str(touro)+" | "+str(ativo_datetime)[10:]+"\n"+str(notc)+"\n\n"
			MsgTo.send_msg(msg,idd,token)
				
	def cataloga(API,trend,par, dias, prct_call, prct_put, timeframe, data_atual):
		data = []
		datas_testadas = []
		time_ = time()
		sair = False
		while sair == False:
			if int(timeframe) >= 4 and  int(timeframe)  <= 7:
				v = 86400
			elif int(timeframe)  <= 3:
				v = 432000
			elif int(timeframe) >= 8 and  int(timeframe)  <= 15:
				v = 28800
			else:
				v = 1000
			velas = API.get_candles(par, (int(timeframe) * 60),v, data_atual)
			if velas != None:
				velas.reverse()
				posicao = 0
				for x in velas:
					try:
						if datetime.fromtimestamp(x['from']).strftime('%Y-%m-%d') != data_atual:
							if datetime.fromtimestamp(x['from']).strftime('%Y-%m-%d') not in datas_testadas:
								datas_testadas.append(datetime.fromtimestamp(x['from']).strftime('%Y-%m-%d'))

							if len(datas_testadas) <= dias:
								x.update({'cor': 'verde' if x['open'] < x['close'] else 'vermelha' if x['open'] > x['close'] else 'doji'})
								if trend == 'ON':
									velas_tendencia = velas[posicao:posicao + prct_call]
									tendencia = controlCatalog.Verificar_Tendencia(velas_tendencia,timeframe,prct_call)
									x.update({'tendencia': tendencia})
									data.append(x)
								else:
									data.append(x)
							else:
								sair = True
								break
						posicao += 1
					except Exception as a:
						#print(a)
						pass

				data_atual = int(velas[-1]['from'] - 1)
			else:
				sair =True
				data = None
		if data != None:
			analise = {}
			for velas in data:
				horario = datetime.fromtimestamp(velas['from']).strftime('%H:%M')
				if horario not in analise:
					analise.update({horario: {'verde': 0, 'vermelha': 0, 'doji': 0, '%': 0, 'dir': '', 'tendencia': 0, 'contra_verde': 0, 'contra_vermelha': 0}})
				analise[horario][velas['cor']] += 1
				if trend == 'ON':
					if velas['cor'] != velas['tendencia']:
						if velas['cor'] == 'verde':
							analise[horario]['contra_verde'] += 1
						else:
							analise[horario]['contra_vermelha'] += 1

				try:
					analise[horario]['%'] = round(100 * (analise[horario]['verde'] / (analise[horario]['verde'] + analise[horario]['vermelha'] + analise[horario]['doji'])))
				except:
					pass

			for horario in analise:
				if analise[horario]['%'] > 50: analise[horario]['dir'] = 'CALL'
				if analise[horario]['%'] < 50: analise[horario]['%'], analise[horario]['dir'] = 100 - analise[horario]['%'], 'PUT '
				if trend == 'ON':
					try:
						if analise[horario]['dir'] == 'CALL':
							analise[horario]['tendencia'] = int(100 - ((analise[horario]['contra_verde'] / analise[horario]['verde']) * 100))
						else:
							analise[horario]['tendencia'] = int(100 - ((analise[horario]['contra_vermelha'] / analise[horario]['vermelha']) * 100))
					except:
						pass
						analise[horario]['tendencia'] = 0

			return analise
		else:
			return None
	
	def Verificar_Tendencia(velas_tendencia,timeframe,prct_call):
		fechamento = round(velas_tendencia[0]['close'], 4)
		df = pd.DataFrame(velas_tendencia)
		EMA = df['close'].ewm(span=prct_call,min_periods=int(timeframe), adjust=False).mean()
		for data in EMA:
			EMA_line = data

		if EMA_line > fechamento:
			dir = 'vermelha'
		elif fechamento > EMA_line:
			dir = 'verde'
		else:
			dir = False

		return dir
	
	def Obter_Paridades(inpPares,typs,API):
		P = API.get_all_open_time()
		paridades = []
		if typs == "free":
			for pares in inpPares:
				if P['digital'][pares]['open'] == True:
					paridades.append(pares)
			for pares in inpPares:
				if P['turbo'][pares]['open'] == True:
					paridades.append(pares)
		else:
			if 'TODOS' in inpPares and 'ABERTOS' in inpPares:
				for pares in P['digital']:
					if P['digital'][pares]['open'] == True:
						paridades.append(pares)
				for pares in P['turbo']:
					if P['turbo'][pares]['open'] == True:
						paridades.append(pares)
			elif "TODOS" in inpPares:
				for pares in P['digital']:
					paridades.append(pares)
				for pares in P['turbo']:
					paridades.append(pares)
			elif 'TODOS' not in inpPares and 'ABERTOS' in inpPares:
				for pares in P['digital']:
					if P['digital'][pares]['open'] == True:
						paridades.append(pares)
				for pares in P['turbo']:
					if P['turbo'][pares]['open'] == True:
						paridades.append(pares)
			else:
				paridades = []
				for pares in inpPares:
					paridades.append(pares)


		return np.unique(paridades)
	
	def Obter_Horario_Paridades():
		info_binarias = {}
		info_digitais = {}
		url = 'https://fininfo.iqoption.com/api/graphql'
		arquivo_payload = open('payload_post.txt', 'r')
		requisicao = requests.post(url, data=arquivo_payload)
		dados = json.loads(requisicao.text)
		for data in dados['data']['BinaryOption']:
			if data['type'] == 'Forex' and len(data['schedule']) != 0:
				x = []
				y = {}
				paridade = data['name']
				y['data'] = data['schedule'][0]['from'].split('T')[0]
				y['abertura'] = data['schedule'][0]['from'].split('T')[1].split('-')[0]
				y['fechamento'] = data['schedule'][0]['to'].split('T')[1].split('-')[0]
				x = [y]
				paridade = controlCatalog.String_Format(paridade)
				info_binarias[paridade] = x

		for data in dados['data']['DigitalOption']:
			if data['type'] == 'Forex' and len(data['schedule']) != 0:
				x = []
				y = {}
				paridade = data['name']
				y['data'] = data['schedule'][0]['from'].split('T')[0]
				y['abertura'] = data['schedule'][0]['from'].split('T')[1].split('-')[0]
				y['fechamento'] = data['schedule'][0]['to'].split('T')[1].split('-')[0]
				x = [y]
				paridade = controlCatalog.String_Format(paridade)
				info_digitais[paridade] = x

		return info_binarias, info_digitais

	def String_Format(string_par):
		format_string = string_par.replace('/', '')
		if re.match("[A-Z]{6} .{5}", format_string):
			format_string = format_string.split(' ')
			format_string = format_string[0] + '-OTC'

		return format_string
	
	def Valida_Sinal(info_binarias, info_digitais, horario, paridade, data_atual):
		if paridade in info_binarias:
			if data_atual == info_binarias[paridade][0]['data']:
				abertura = info_binarias[paridade][0]['abertura']
				fechamento = info_binarias[paridade][0]['fechamento']
				# dif_abertura: Retorna um numero positivo caso o horario do sinal seja maior que o horario de abertura da paridade. Ex: Horario do sinal 01:15 e abertura da paridade é de 01:00, irá retornar 15, que é a diferença em minutos.
				dif_abertura = int((datetime.strptime(horario, '%H:%M') - datetime.strptime(abertura, '%H:%M:%S')).total_seconds() / 60)
				# dif_fechamento: O inverso de dif_abertura. retorna um numero negativo (que é a diferença em minutos) se o horario do sinal for menor que o horario de fechamento da paridade.
				dif_fechamento = int((datetime.strptime(horario, '%H:%M') - datetime.strptime(fechamento, '%H:%M:%S')).total_seconds() / 60)
				# Verifica se o sinal esta dentro do horario de funcionamento da paridade, e retorna True caso esteja.
				if dif_abertura > 0 and dif_fechamento < 0:
					return True

		if paridade in info_digitais:
			if data_atual == info_digitais[paridade][0]['data']:
				abertura = info_digitais[paridade][0]['abertura']
				fechamento = info_digitais[paridade][0]['fechamento']
				# dif_abertura: Retorna um numero positivo caso o horario do sinal seja maior que o horario de abertura da paridade. Ex: Horario do sinal 01:15 e abertura da paridade é de 01:00, irá retornar 15, que é a diferença em minutos.
				dif_abertura = int((datetime.strptime(horario, '%H:%M') - datetime.strptime(abertura, '%H:%M:%S')).total_seconds() / 60)
				# dif_fechamento: O inverso de dif_abertura. retorna um numero negativo (que é a diferença em minutos) se o horario do sinal for menor que o horario de fechamento da paridade.
				dif_fechamento = int((datetime.strptime(horario, '%H:%M') - datetime.strptime(fechamento, '%H:%M:%S')).total_seconds() / 60)
				# Verifica se o sinal esta dentro do horario de funcionamento da paridade, e retorna True caso esteja.
				if dif_abertura > 0 and dif_fechamento < 0:
					return True
		# Retorna False caso não satisfaça nenhuma condição
		return False
	
	def Escreve_Arquivo(arquivo_saida, timeframe, par, horario, direcao, data_atual, martingale):
		open(arquivo_saida, 'a').write('M' + str(timeframe) + ';' + par + ';' + horario + ':00;' + direcao + '\n')
	
	def catalog(API,typs,inpDias,inpDPrct,inpGales,inpPares,inpTimes,valiteSignal,trend,trendPrct,arqname,idd,API_TOKEN,date,dir):
		sinais = ''
		paridades = controlCatalog.Obter_Paridades(inpPares,typs,API) 
		arquivo_saida = arqname+'.txt'
		check_lista = 'N'
		prctCall = int(inpDPrct)
		data_atual = tnumericos(date,0)
		prctPut = int(inpDPrct)
		#info_binarias, info_digitais = controlCatalog.Obter_Horario_Paridades()
		for timeframe in inpTimes:
			catalogacao = {}
			for par in paridades:
				if par != "TODOS":
					catalogacao.update({par: controlCatalog.cataloga(API,trend,par, inpDias, prctCall, prctPut, timeframe, data_atual)})
					if catalogacao[par] != None:
						for par in catalogacao:
							for horario in sorted(catalogacao[par]):
								if str(inpGales).strip() != '':
									mg_time = horario
									soma = {'verde': catalogacao[par][horario]['verde'], 'vermelha': catalogacao[par][horario]['vermelha'], 'doji': catalogacao[par][horario]['doji']}
									for i in range(int(inpGales)):
										catalogacao[par][horario].update({'mg' + str(i + 1): {'verde': 0, 'vermelha': 0, 'doji': 0, '%': 0}})
										mg_time = str(datetime.strptime((dateTimeNowFordate()).strftime('%Y-%m-%d ') + str(mg_time), '%Y-%m-%d %H:%M') + timedelta(minutes=int(timeframe)))[11:-3]
										if mg_time in catalogacao[par]:
											catalogacao[par][horario]['mg' + str(i + 1)]['verde'] += catalogacao[par][mg_time]['verde'] + soma['verde']
											catalogacao[par][horario]['mg' + str(i + 1)]['vermelha'] += catalogacao[par][mg_time]['vermelha'] + soma['vermelha']
											catalogacao[par][horario]['mg' + str(i + 1)]['doji'] += catalogacao[par][mg_time]['doji'] + soma['doji']
											catalogacao[par][horario]['mg' + str(i + 1)]['%'] = round(100 * (catalogacao[par][horario]['mg' + str(i + 1)]['verde' if catalogacao[par][horario]['dir'] == 'CALL' else 'vermelha'] / (catalogacao[par][horario]['mg' + str(i + 1)]['verde'] + catalogacao[par][horario]['mg' + str(i + 1)]['vermelha'] + catalogacao[par][horario]['mg' + str(i + 1)]['doji'])))
											soma['verde'] += catalogacao[par][mg_time]['verde']
											soma['vermelha'] += catalogacao[par][mg_time]['vermelha']
											soma['doji'] += catalogacao[par][mg_time]['doji']
										else:
											catalogacao[par][horario]['mg' + str(i + 1)]['%'] = 0
										
					else:
						MsgTo.send_msg("Não foi possivel catalogar o par"+str(par),idd,API_TOKEN)
						del catalogacao[par]
			for par in catalogacao:
				if par != "TODOS":
					for horario in sorted(catalogacao[par]):
						if par != "TODOS":
							ok = False
							if trend == 'ON':
								if catalogacao[par][horario]['tendencia'] >= trendPrct and catalogacao[par][horario]['%'] >= inpDPrct:
									ok = True
							else:
								if catalogacao[par][horario]['%'] >= inpDPrct:
									ok = True
								else:
									for i in range(int(inpGales)):
										if catalogacao[par][horario]['mg' + str(i + 1)]['%'] >= inpDPrct:
											ok = True
											break
							if ok == True:
								direcao = catalogacao[par][horario]['dir'].strip()
								if dir == "CALL":
									if direcao == "CALL":
										sinais+= "M"+str(timeframe)+";"+par+";"+horario+":00;CALL\n"
								elif dir == "PUT":
									if dir =="PUT":
										sinais+= "M"+str(timeframe)+";"+par+";"+horario+":00;PUT\n"
								else:
									if direcao == "CALL":
										sinais+= "M"+str(timeframe)+";"+par+";"+horario+":00;CALL\n"	
									else:
										sinais+= "M"+str(timeframe)+";"+par+";"+horario+":00;PUT\n"

						
		try:
			with open(arquivo_saida, 'w') as arquivo:
				arquivo.write(sinais)
				arquivo.close()
			MsgTo.upload_file(arquivo_saida,idd,API_TOKEN)
			sleep(2)
			os.remove(arquivo_saida)
		except:	
			pass
		MsgTo.send_msg("FINALIZADO ",idd,API_TOKEN)