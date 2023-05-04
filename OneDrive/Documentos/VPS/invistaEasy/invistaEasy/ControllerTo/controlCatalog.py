from datetime import datetime, timedelta
from time import sleep, time
from ControllerTo.cantrolDate import tnumericos,dateTimeNowFordate,dateTimeNowForString,dateTimeNowForStringPlus
import json,re,requests
import pandas as pd
import numpy as np
from Controller.controlDao import connectDao
from iqoptionapi.stable_api import IQ_Option
from telegram import ParseMode
from bs4 import BeautifulSoup
import os
import telegram
import json
from iqoptionapi.constants import ACTIVCATALAGVn, ACT,pares
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
		try:
			if API_TOKEN != None:
				bot = telegram.Bot(token=API_TOKEN)
				bot.sendMessage(parse_mode=ParseMode.HTML, chat_id=idd, text='' + texto + '')
		except Exception as a:
			MsgTo.send_msg(str(idd)+" WINLAB "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
			pass

class controlCatalogTre:
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
			if timeF < 2:
				for p in P['turbo']: 
					if P['turbo'][p]['open']: 
						try:
							pares['pares']['turbo'].update({p: d[p]['turbo']})
							sleep(0.1)
						except:
							pass

					elif P['turbo'][p]['open'] == False and p in pares['pares']['turbo']:
							del pares['pares']['turbo'][p]
			if timeF > 1:
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

		if timeF > 1:
			for par in pares['pares']['binary']:
				if par not in pair and par in ACT:
					pair.append(par)
		else:
			for par in pares['pares']['turbo']:
				if par not in pair and par in ACT:
					pair.append(par)	
		for par in pares['pares']['digital']:
			if par not in pair and par in ACT:
				pair.append(par)	
		if pairs != None:
			if pairs in pair:
				pair.clear()
				pair.append(pairs)
			else:
				return False
		return pair
	def catalogAnaly(telegramTk,idd,pair,analysePct,timeF,filtro,sistema,user):
		API=IQ_Option("ridev97046@whyflkj.com","j3100davi")
		API.connect()
		API.check_connect()
		
		def catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,areason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_mhi_maioria',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['00','05','10','15','20','25','30','35','40','45','50','55']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						areason = areason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(areason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass		
		
		def catalogacao_forca_maioria(API,telegramTk,idd,par,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_forca_maioria',analysePct,sistema)	
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['00','05','10','15','20','25','30','35','40','45','50','55']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_forca_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_forca_minoria',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['00','05','10','15','20','25','30','35','40','45','50','55']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass

		def catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_mhi_minoria',analysePct,sistema)
					if check:	
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['00','05','10','15','20','25','30','35','40','45','50','55']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
				
		def catalogacao_mhi_minoria_2(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_mhi_minoria_2',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['01','06','11','16','21','26','31','36','41','46','51','56']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_mhi_minoria_3(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_mhi_minoria_3',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['02','07','12','17','22','27','32','37','42','47','52','57']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_legado_ancestral(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_legado_ancestral',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['02','07','12','17','22','27','32','37','42','47','52','57']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass	
		
		def catalogacao_tres_mosqueteiros(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema): 
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_tres_mosqueteiros',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['03','08','13','18','23','28','33','38','43','48','53','58']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_torres_gemeas(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_torres_gemeas',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['04','09','14','19','24','29','34','39','44','49','54','59']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_motim_triplo(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_motim_triplo',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['04','09','14','19','24','29','34','39','44','49','54','59']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
			
		def catalogacao_repeticao_final(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_repeticao_final',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['04','09','14','19','24','29','34','39','44','49','54','59']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_repeticao_primaria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_repeticao_primaria',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['01','06','11','16','21','26','31','36','41','46','51','56']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_eter(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_eter',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['04','09','14','19','24','29','34','39','44','49','54','59']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass		
		
		def catalogacao_forca_maioria_5(API,telegramTk,idd,par,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_forca_maioria',analysePct,sistema)	
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['00','30']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_forca_minoria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_forca_minoria',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['00','30']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass

		def catalogacao_mhi_minoria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,reason = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_mhi_minoria',analysePct,sistema)
					if check:	
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:]  in ['00','30']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = reason.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_torres_gemeas_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_torres_gemeas',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['25','55']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_repeticao_final_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_repeticao_final',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['20','50']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_hat_trick(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):	
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_hat_trick',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['10','25','40','55']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_insurgente(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_insurgente',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['10','25','40','55']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogaca_vela_surpresa(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogaca_vela_surpresa',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['00','15','30','45']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_vira_casaca2(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_vira_casaca_2',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['00']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		def catalogacao_vira_casaca(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema):
			try:
				for par in pares:
					check,a = connectDao.updateStrategy(par,timeF,filtro,'catalogacao_vira_casaca',analysePct,sistema)
					if check:
						xxss = 0
						while True:
							xxss += 1
							dt = dateTimeNowForStringPlus(xxss)
							if dt[3:] in ['00']:
								timepx = 'Próxima Entrada: '+str(dt)
								break
							
						reason = a.replace('Próxima Entrada:',timepx)
						MsgTo.send_msg(reason,idd,telegramTk)	
			except Exception as a:
				MsgTo.send_msg('MS ALLWINLAB\n'+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
				pass
		
		pares = controlCatalogTre.get_pares(API,int(timeF),pair)
		if pair != None  and pares != False :
			if pair in pares:
				pares = [pair]
			else:
				pares = False
		if pares != False:
			if timeF == 1:
				if sistema == None:
					if user == 'free':
						catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,"MHI-MAIORIA")
						catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MHI')
					else:
						catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,"MHI-MAIORIA")
						catalogacao_forca_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MILHÃO MAIORIA')
						catalogacao_forca_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MILHÃO MINORIA')
						catalogacao_mhi_minoria_2(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MHI-2')
						catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MHI')
						catalogacao_tres_mosqueteiros(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,"3 MOSQUETEIROS")
						catalogacao_torres_gemeas(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,"TORRES GÊMEAS")
						catalogacao_repeticao_final(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'3 VIZINHOS')
						catalogacao_repeticao_primaria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'PADRÃO 23')
						catalogacao_eter(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'5º ELEMENTO')
						catalogacao_mhi_minoria_2(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MHI-2')
						catalogacao_mhi_minoria_3(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MHI-3')
						catalogacao_legado_ancestral(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MELHOR DE 3')
						catalogacao_motim_triplo(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'PADRÃO 3 X 1')
				elif 'MHI' == sistema:
					catalogacao_mhi_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif "MHI-MAIORIA" in sistema:
					catalogacao_mhi_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif "TORRES GÊMEAS" in sistema:
					catalogacao_torres_gemeas(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif "3 MOSQUETEIROS" in sistema:
					catalogacao_tres_mosqueteiros(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif '3 VIZINHOS' == sistema:
					catalogacao_repeticao_final(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'PADRÃO 23' == sistema:
					catalogacao_repeticao_primaria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif '5º ELEMENTO' == sistema:
					catalogacao_eter(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'MHI-2' == sistema:
					catalogacao_mhi_minoria_2(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'MHI-3' == sistema:
					catalogacao_mhi_minoria_3(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'MELHOR DE 3' == sistema:
					catalogacao_legado_ancestral(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'MILHÃO MAIORIA' == sistema:
					catalogacao_forca_maioria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'MILHÃO MINORIA' == sistema:
					catalogacao_forca_minoria(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'PADRÃO 3 X 1' == sistema:
					catalogacao_motim_triplo(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
			elif timeF == 5: 
				if sistema == None:
					catalogacao_forca_maioria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MILHÃO MAIORIA')
					catalogacao_forca_minoria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MILHÃO MINORIA')
					catalogacao_mhi_minoria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'MHI')
					catalogacao_torres_gemeas_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,"TORRES GÊMEAS")
					catalogacao_repeticao_final_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'3 VIZINHOS')
					catalogacao_hat_trick(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'TRIPLICAÇÃO')
					catalogacao_insurgente(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'NÃO TRIPLICAÇÃO')
					catalogaca_vela_surpresa(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,'FORÇA MENOR 15')
				elif 'MHI' == sistema:
					catalogacao_mhi_minoria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif "TORRES GÊMEAS" in sistema:
					catalogacao_torres_gemeas_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif '3 VIZINHOS' == sistema:
					catalogacao_repeticao_final_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'MILHÃO MAIORIA' == sistema:
					catalogacao_forca_maioria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'MILHÃO MINORIA' == sistema:
					catalogacao_forca_minoria_5(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'TRIPLICAÇÃO' == sistema:
					catalogacao_hat_trick(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'NÃO TRIPLICAÇÃO' == sistema:
					catalogacao_insurgente(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif 'FORÇA MENOR 15' == sistema:
					catalogaca_vela_surpresa(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
			elif timeF == 15:
				if sistema == None:
					catalogacao_vira_casaca2(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
					catalogacao_vira_casaca(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif '1-VIRA CASACA' == sistema:
					catalogacao_vira_casaca(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)
				elif "2-VIRA C. MHI"  == sistema:
					catalogacao_vira_casaca2(API,telegramTk,idd,pair,analysePct,timeF,filtro,pares,sistema)

			MsgTo.send_msg('PRONTO AÍ ESTÃO TODAS AS ESTRATÈGIAS COM OS SEUS PARÂMETROS.',idd,telegramTk)
		else:
			MsgTo.send_msg('PAR ESTÁ FECHADO.',idd,telegramTk)

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
									tendencia = controlCatalogTre.Verificar_Tendencia(velas_tendencia,timeframe,prct_call)
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
				paridade = controlCatalogTre.String_Format(paridade)
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
				paridade = controlCatalogTre.String_Format(paridade)
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
		paridades = controlCatalogTre.Obter_Paridades(inpPares,typs,API) 
		arquivo_saida = arqname+'.txt'
		check_lista = 'N'
		prctCall = int(inpDPrct)
		data_atual = tnumericos(date,0)
		prctPut = int(inpDPrct)
		#info_binarias, info_digitais = controlCatalogTre.Obter_Horario_Paridades()
		for timeframe in inpTimes:
			catalogacao = {}
			for par in paridades:
				if par != "TODOS":
					catalogacao.update({par: controlCatalogTre.cataloga(API,trend,par, inpDias, prctCall, prctPut, timeframe, data_atual)})
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
