from datetime import datetime, timedelta
from time import sleep, time
import json,re,requests
import pandas as pd
import numpy as np
from telegram import ParseMode
from bs4 import BeautifulSoup
import os
import telegram
import json
from iqoptionapi.constants import Activ
import requests
from time import sleep
from threading import Lock
from datetime import datetime, timedelta, date
from logging import disable, DEBUG, ERROR
from configparser import RawConfigParser
from time import sleep, time, mktime
from warnings import filterwarnings
from threading import Thread
from dateutil import tz
import traceback, sys, json
disable(level=DEBUG)
disable(level=ERROR)

class MsgTo:
	def upload_file(file,idd,API_TOKEN):
		try:
			config = {'url': 'https://api.telegram.org/bot'+API_TOKEN+'/', 'lock': Lock(), 'url_file': 'https://api.telegram.org/file/bot'+API_TOKEN+'/'}
			formatos = {'png': {'metodo': 'sendPhoto', 'send': 'photo'},
						'text': {'metodo': 'sendDocument', 'send': 'document'},
						'pdf': {'metodo': 'sendDocument', 'send': 'document'}}
			return requests.post(config['url'] + formatos['text' if '.txt' in file else 'png']['metodo'], {'chat_id': idd}, files={formatos['text' if '.txt' in file else 'png']['send']: open(file, 'rb')}).text
		except:
			pass
	def send_msg(texto,idd,API_TOKEN):
		try:
			bot = telegram.Bot(token=''+API_TOKEN+'')
			bot.sendMessage(parse_mode=ParseMode.HTML, chat_id=idd, text=texto)
		except:
			pass

class controlCatalogTo:
	def get_pares(API,conf):
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
			for a in ['YANDEX'   ,'JPM'   ,'SNAP'   ,'MORSTAN'   ,'TWITTER'   ,'GS'   ,'BAIDU'   ,'COKE'   ,'GOOGLE'   ,'FACEBOOK'   ,'APPLE'   ,'ALIBABA'   ,'INTEL'   ,'NIKE'  ,'AMAZON'   ,'CITI'  ,'MSFT' ,'USDJPY'   ,'AIG' ,'TESLA'   ,'MCDON']:
				try:
					conf['pares'].remove(a)
				except:
					pass
			del P
		return conf
	def escArquivo(ARQUIVO, TEXTO, wut='a'):
		configs = open(ARQUIVO, wut)
		configs.write(str(TEXTO))
		configs.close()
		MsgTo.send_msg(TEXTO,'971655878','5124752583:AAGiNacB-BtUCnxik1_Ek3VQRmmTr0sFJvU')
	
	def save_signal(data,conf):
		name = 'sinais_' + datetime.now().strftime('%d-%m') + '_' + str(conf['timeframe_analise']) + 'M_' + str(conf['martingale']) + 'MG.html'
		controlCatalogTo.escArquivo(name, '', 'w+')
		base = '<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><title>Catalogador</title><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"></head><body><center><table class="table" id="data">_?_'
		cabecalho = '<tr><th scope="col">DEL</th><th scope="col">ID</th><th scope="col">HORA</th><th scope="col">PARIDADE</th><th scope="col">DIRECAO_</th><th scope="col">%</th><th scope="col">MAO FIXA</th> MG </tr> '
		if int(conf['martingale']) > 0:
			for i in range(int(conf['martingale'])):
				cabecalho = cabecalho.replace(' MG ', '<th scope="col">MARTINGALE ' + str(i + 1) + '</th><th scope="col">%</th> MG ')

		base = base.replace('_?_', cabecalho.replace(' MG ', '') + '_?_')
		info = ''
		for ns in data:
			info = info + '<tr><td><button type="button" class="deletebtn" title="Remover">X</button></td><td scope="row">' + str(ns) + '</td>'
			for x in data[ns]:
				if 'mg' in x:
					for ll in data[ns][x]:
						info = info + '<td>' + str(data[ns][x][ll]).replace('"', "'") + '</td>'

				else:
					info = info + '<td> ' + str(data[ns][x]).replace('"', "'") + '</td>'

			info = info + '</tr>'

		controlCatalogTo.escArquivo(name, base.replace('_?_', info) + '<button type="button" id="save_files">SALVAR SINAIS</button></table></center><script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script><script>$(document).ready(function(){ var save_file = function(){\tvar l = \'\'; var itArr = \'\'; var tbl2 = $(\'#data tr\').each(function(i) { x = $(this).children();\tx.each(function() {\tl = $(this).text();\tif (l.indexOf(\':\') > 0) { itArr = itArr + l + \',\';  } else if (l.indexOf(\'CALL\') > 0) { itArr = itArr + l + \'\\r\\n\'; } else if (l.indexOf(\'PUT\') > 0) { itArr = itArr + l + \'\\r\\n\'; } else if (l.length == 7) { itArr = itArr + l + \',\'; }  else if (l.indexOf(\'-OTC\') > 0) { itArr = itArr + l + \',\'; } }); }); const textToBLOB = new Blob([itArr], { type: \'text/plain\' }); const sFileName = \'sinais.txt\'; let newLink = document.createElement("a"); newLink.download = sFileName; if (window.webkitURL != null) { newLink.href = window.webkitURL.createObjectURL(textToBLOB); }else{ newLink.href = window.URL.createObjectURL(textToBLOB); newLink.style.display = "none"; document.body.appendChild(newLink); } newLink.click(); }\n$(\'#save_files\').on(\'click\', save_file); $(document).on("click", "button.deletebtn", function () {$(this).closest("tr").remove();return false;}); }); </script></body></html>')

	def is_number(d):
		try:
			float(d)
			return True
		except ValueError:
			return False
		except TypeError:
			return False

	def Noticias(idd,API_TOKEN):
		noticias = 0
		from bs4 import BeautifulSoup
		import requests
		#MsgTo.send_msg("🤖:Analisando noticias, aguarde.. ",idd,API_TOKEN)
		headers = requests.utils.default_headers()
		headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
		data = requests.get('https://br.investing.com/economic-calendar/', headers=headers)
		if data.status_code == requests.codes.ok:
			page = BeautifulSoup(data.text, 'html.parser')
			blocos = page.find('table', {'id': 'economicCalendarData'}).find('tbody').findAll('tr', {'class': 'js-event-item'})
			result = {}
			for blocos2 in blocos:
				impacto = str(blocos2.find('td', {'class': 'sentiment'}).get('data-img_key')).replace('bull', '')
				_datetime = str(blocos2.get('data-event-datetime')).replace('/', '-')
				par = blocos2.find('td', {'class': 'left flagCur noWrap'}).text.strip()
				if int(impacto) > 0:
					if par != '':
						if _datetime != '':
							sleep(0.1)
							hora_obj = datetime.strptime(str(_datetime), '%Y-%m-%d %H:%M:%S')
							timestamps = [int(mktime((hora_obj - timedelta(seconds=(int(noticias) * 60))).timetuple())), int(mktime((hora_obj + timedelta(seconds=(int(noticias) * 60))).timetuple()))]
				if par not in result:
					result.update({par: []})
					result[par].append(timestamps)
				else:
					if timestamps not in result[par]:
						result[par].append(timestamps)
		else:
			noticias = 'N'
		#MsgTo.send_msg("🤖:Analise finalizada",idd,API_TOKEN)
		return result

	def timestamp_converter(x, retorno=1):
		hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
		hora = hora.replace(tzinfo=(tz.gettz('GMT')))
		if retorno == 1:
			return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]
		return hora.astimezone(tz.gettz('America/Sao Paulo'))

	def pega_velas(API,ns,conf,idd,API_TOKEN, par=None):
		time_start = int(time())
		dias = {}
		time_ = time()
		xeit = []
		bruto = []
		#MsgTo.send_msg("🤖:Analisando " + str(par) + ", aguarde.. ",idd,API_TOKEN)
		while len(xeit) <= int(conf['dias_analise']) + 4:
			x = ''
			while x == '':
				x = API.get_candles(par, int(conf['timeframe_analise']) * 60, 1000, time_)		
			bruto = x + bruto
			time_ = int(x[0]['from']) - 1
			for lets in x:
				if len(xeit) > int(conf['dias_analise']) + 4:
					break
				else:
					YY = str(str(controlCatalogTo.timestamp_converter(lets['from'])))[:-9]
				if YY not in xeit:
					xeit.append(YY)		
		d = sorted(xeit)[0]
		del xeit
		#MsgTo.send_msg("🤖:Analisando " +par+ ", aguarde.. 1º analise",idd,API_TOKEN)
		for data in bruto:
			cor = 'vermelho' if data['open'] > data['close'] else 'verde' if data['open'] < data['close'] else 'cinza'
			dias.update({str(controlCatalogTo.timestamp_converter(data['from'])): {'cor':cor,  'min':data['min'],  'max':data['max'],  'open':data['open'],  'close':data['close']}})		
		del bruto
		candle = {}
		#MsgTo.send_msg("🤖:Analisando " +par+ ", aguarde.. 2º analise",idd,API_TOKEN)
		for data_dia in dias:
			hora = str(data_dia)[11:-3]
			if hora not in candle:
				candle.update({str(hora): {'vermelho':0,  'verde':0,  'cinza':0,  '%':0,  'dir':'',  'ultima_cor':'',  'quantia':0,  'cores':'',  'ohlc':{}}})
			for i in range(1, conf['martingale'] + 1):
				if 'mg' + str(i) not in candle[hora]:
					candle[hora].update({'mg' + str(i): ''})		
			candle[hora]['ohlc'].update({str(time()): {'open':dias[data_dia]['open'],  'max':dias[data_dia]['max'],  'min':dias[data_dia]['min'],  'close':dias[data_dia]['close']}})
			candle[hora][dias[data_dia]['cor']] += 1
			candle[hora]['cores'] += dias[data_dia]['cor'] + ' '
			candle[hora]['quantia'] += 1
			if candle[hora]['quantia'] > int(conf['dias_analise']):
				candle[hora][candle[hora]['cores'].split(' ')[0]] -= 1
				candle[hora]['cores'] = candle[hora]['cores'].replace(candle[hora]['cores'].split(' ')[0] + ' ', '', 1)
				candle[hora]['quantia'] -= 1
				for i in candle[hora]['ohlc']:
					del candle[hora]['ohlc'][i]
					break		
			candle[hora]['%'] = int(100 * ((candle[hora]['vermelho'] if candle[hora]['vermelho'] > candle[hora]['verde'] else candle[hora]['verde']) / candle[hora]['quantia']))
			candle[hora]['dir'] = 'PUT' if candle[hora]['vermelho'] > candle[hora]['verde'] else 'CALL' if candle[hora]['verde'] > candle[hora]['vermelho'] else ''
			candle[hora]['ultima_cor'] = dias[data_dia]['cor']
			try:
				for i in range(1, conf['martingale'] + 1):
					tt = str((datetime.strptime(str(data_dia).strip(), '%Y-%m-%d %H:%M:%S') + timedelta(seconds=(i * (int(conf['timeframe_analise']) * 60)))).strftime('%Y-%m-%d %H:%M:%S'))
					candle[hora]['mg' + str(i)] = candle[hora][('mg' + str(i))] + dias[tt]['cor'] + '|' + datetime.strptime(tt, '%Y-%m-%d %H:%M:%S').strftime('%d/%m %H:%M').replace(' ', '_') + ' '
					mg_divide = candle[hora][('mg' + str(i))].split(' ')
					if len(mg_divide) > int(conf['dias_analise']) + 1:
						candle[hora]['mg' + str(i)] = candle[hora][('mg' + str(i))].replace(mg_divide[0] + ' ', '', 1)
					else:
						candle[hora]['mg' + str(i)] = candle[hora][('mg' + str(i))].replace('  ', ' ')		
			except:
				pass		
		MsgTo.send_msg('🤖:Analise finalizada! - ' + par+ ' -  ⏱' + str(int(time()) - time_start) + ' segundos⏱',idd,API_TOKEN)
		
		return candle
	
	def catalog(API,conf,arqname,idd,API_TOKEN,notici,minNot):
		arquivo_saida = arqname+'.txt'
		CAT = {}
		if'ABERTOS' in conf['pares']:
			conf['pares'] = []
			conf = controlCatalogTo.get_pares(API,conf)

		
		for ns, par in enumerate(conf['pares']):
			if par not in CAT:
				ns += 1
				CAT.update({par: controlCatalogTo.pega_velas(API,ns, conf,idd,API_TOKEN,par)})
		noticias = controlCatalogTo.Noticias(idd,API_TOKEN)
		ns = 1
		data = {}
		a = ''
		for par in CAT:
			for hora in sorted(CAT[par]):
				filtro = True
				if noticias != 'NÃO':
					fc = int(datetime.timestamp(datetime.strptime(hora + ':00 ' + datetime.now().strftime(' %d.%m.%Y'), '%H:%M:%S %d.%m.%Y')))
					for par_noticia in noticias:
						if filtro == False:
							break
						if par_noticia in par:
							for timestamp in noticias[par_noticia]:
								if timestamp[0] <= fc:
									if timestamp[1] >= fc:
										filtro = False
										break

				if filtro:
					cor_predominante = 'VERDES' if CAT[par][hora]['vermelho'] < CAT[par][hora]['verde'] else 'VERMELHAS'
					if conf['martingale'] > 0:
						for i in range(1, int(conf['martingale']) + 1):
							if filtro == False:
								break
							try:
								if controlCatalogTo.is_number(int(conf['porcentagem_gale'])):
									if round((CAT[par][hora][('mg' + str(i))].count('vermelho' if cor_predominante == 'VERMELHAS' else 'verde') + (1 if cor_predominante == 'VERMELHAS' else 0)) / len(CAT[par][hora][('mg' + str(i))].split(' ')) * 100) < int(conf['porcentagem_gale']) or ('cinza' in CAT[par][hora][('mg' + str(i))]):
										filtro = False
							except Exception as xsxsxs:
								pass

				if CAT[par][hora]['%'] >= float(conf['porcentagem_mao_fixa']):
					if 'cinza' not in CAT[par][hora]['cores']:
						if filtro:
							prct = round(CAT[par][hora]['%'])
							data.update({ns: {'hora':hora,  'par':par,  'direcao':'PUT' if cor_predominante == 'VERMELHAS' else 'CALL',  '%':prct,  'mao fixa':''}})
							
							for c in CAT[par][hora]['cores'].split():
								data[ns]['mao fixa'] = data[ns]['mao fixa'] + ('<font color="red">R</font>' if c == 'vermelho' else '<font color="green">G</font>')
								
							if 'mg1' in CAT[par][hora]:
								for i in CAT[par][hora]:
									if 'mg' in i:
										data[ns].update({i: {'cores':'',  '%':0}})
										#print('' + str(i).replace('mg', '') + 'º'+ ' MÃO: ')
										dale = CAT[par][hora][i].strip().split(' ')
										for index, dale2 in enumerate(dale):
											data[ns][i]['cores'] = data[ns][i]['cores'] + ('<font color="red">R</font>' if 'vermelho' in dale2 else '<font color="green">G</font>')
											
										data[ns][i]['%'] = round(CAT[par][hora][i].count('vermelho' if cor_predominante == 'VERMELHAS' else 'verde') / len(dale) * 100)

							ns += 1
		if len(data) > 0:
			x = ''
			for details in data:
				#M1;EURJPY-OTC;00:28:00;PUT
				x+= 'M'+str(conf['timeframe_analise'])+';'+ str(data[details]['par'])+';'+data[details]['hora']+':00;'+data[details]['direcao']+'\n'
				a += '🔰'+str(details)+ ' ⌚ '+data[details]['hora']+' 💹 ' + str(data[details]['par'])
				if data[details]['direcao'] == 'PUT':
					a+=' PUT '
					a+='🟥 ' * data[details]['mao fixa'].count('R')
					a+='🟩 ' * data[details]['mao fixa'].count('G')
					a+= str(data[details]['%'])+'%    '
					try:
						a+='🟥 ' * data[details]['mg1']['cores'].count('R')
						a+='🟩 ' * data[details]['mg1']['cores'].count('G')
						a+= str(data[details]['mg1']['%'])+'%\n'
					except:
						pass
				else:
					a+=' CALL '
					a+='🟩 ' * data[details]['mao fixa'].count('G')
					a+='🟥 ' * data[details]['mao fixa'].count('R')
					a+= str(data[details]['%'])+'%    '
					try:
						a+='🟩 ' * data[details]['mg1']['cores'].count('G')
						a+='🟥 ' * data[details]['mg1']['cores'].count('R')
						a+= str(data[details]['mg1']['%'])+'%\n'
					except:
						pass
			sinais = a
			ss = x
			try:
				with open('1'+arquivo_saida, 'w+',encoding='utf8') as arquivo:
					arquivo.write(ss)
					arquivo.close()
				MsgTo.upload_file('1'+arquivo_saida,idd,API_TOKEN)
				sleep(2)
				os.remove('1'+arquivo_saida)
			except Exception as a:
				pass
			#try:
			#	with open(arquivo_saida, 'w+',encoding='utf8') as arquivo:
			#		arquivo.write(sinais)
			#		arquivo.close()
			#	MsgTo.upload_file(arquivo_saida,idd,API_TOKEN)
			#	sleep(2)
			#	os.remove(arquivo_saida)
			#except Exception as a:
			#	print(a)	
			#	pass
			MsgTo.send_msg("FINALIZADO ",idd,API_TOKEN)
			#controlCatalogTo.save_signal(data,conf)
		else:
			MsgTo.send_msg("🤖:Nada encontrado",idd,API_TOKEN)