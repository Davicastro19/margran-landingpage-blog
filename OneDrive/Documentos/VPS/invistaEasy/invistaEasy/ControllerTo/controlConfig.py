from datetime import datetime
from pytz import timezone
import telegram
from iqoptionapi.constants import ACTIVES
from telegram import ParseMode
import json
import pandas as pd
from Controller.controlEnum import MENSAGE

		
		

class MsgTo:
	def send_msg(texto, idd,telegramTk):
		try:
			if telegramTk != None:
				bot = telegram.Bot(token=telegramTk)
				bot.sendMessage(parse_mode=ParseMode.HTML, chat_id=idd, text='' + texto + '')
		except Exception as a:
			pass

class controlOptions:
	def payBin(API,par,time):
		P = ''	
		pay =1
		P = API.get_all_open_time()
		if time <3:
			if type(P) != None:
				d = API.get_all_profit()
				for p in P['turbo']: # Turbo 5 <
					if P['turbo'][p]['open'] and par == p:
						return int(d[p]['turbo'] * 100)
			
			return pay
		else:
			if type(P) != None:
				d = API.get_all_profit()
				for p in P['binary']: # Turbo 5 <
					if P['binary'][p]['open'] and par == p:
						return int(d[p]['binary'] * 100)
			
			return pay

class controlParameter():
	def ValiList(lista):
		try:
			configli = lista.split("\n")
			listt = lista.split("\n")
			for index,a in enumerate(listt):
				if a == '':
					del listt[index]
			for dadoss in listt:
				dados = dadoss.split(';')
				T = dados[0]
				T = str(T)[1:]
				T = int(T)
				P = dados[1].strip()
				H = dados[2].strip()
				D = dados[3].strip()
				if T != 1 and T != 5 and T != 15 and T != 60:
					tex = 'Lista: Tempo não permitido! set - "'+str(T)+''
					listt = []
					result = False
				elif P not in ACTIVES:
					tex = 'Lista: Par não existe! set - "'+P+''
					listt = []
					result = False
				elif controlParameter.validate(H) == False:
					tex = 'Lista: Horario não existe! set - "'+H+''
					listt = []
					result = False
				elif D != "CALL" and D != "PUT":
					tex = 'Lista: Erro na Paridade! set = "'+D+''
					listt = []
					result = False
			if listt != []:
				newline = ""
				for a in configli:
					a = a.split(";")
					T = a[0]
					P = a[1]
					H = a[2]
					D = a[3]
					newline += H+';'+T+';'+P+';'+D+'\n'
				newline = newline.strip()
				newline  = newline.split('\n')
				newli = ""
				for s in sorted(newline):
					newli += str(s)+"\n"
				newli = newli.split("\n")
				sinal = ""
				for index,a in enumerate(newli):
					if a == '':
						del newli[index]
				lista = ""
				for n in newli:
					n = n.split(";")
					T = n[1]
					P = n[2]
					H = n[0]
					D = n[3]
					sinal = T+';'+P+';'+H+';'+D
					lista += sinal+'\n'
					listt = lista.strip()
			return True
		except Exception as a:
			return False
	def ValidaList(lista):
		try:
			tex = ''
			result = False
			configli = lista.split("\n")
			listt = lista.split("\n")
			for index,a in enumerate(listt):
				if a == '':
					del listt[index]
			for dadoss in listt:
				dados = dadoss.split(';')
				T = dados[0]
				T = str(T)[1:]
				T = int(T)
				P = dados[1].strip()
				H = dados[2].strip()
				D = dados[3].strip()
				if T != 1 and T != 5 and T != 15 and T != 60 and T != 30 and T != 10:
					tex = 'Lista: Tempo não permitido! set - "'+str(T)+'"\nerro aqui:'+dadoss+''
					listt = []
					result = False
				elif P not in ACTIVES:
					tex = 'Lista: Par não existe! set - "'+P+'"\nerro aqui:'+dadoss+''
					listt = []
					result = False
				elif controlParameter.validate(H) == False:
					tex = 'Lista: Horario não existe! set - "'+H+'"\nerro aqui:'+dadoss+''
					listt = []
					result = False
				elif D != "CALL" and D != "PUT":
					tex = 'Lista: Erro na Paridade! set = "'+D+'"\nerro aqui:'+dadoss+''
					listt = []
					result = False
			if listt != []:
				newline = ""
				for a in configli:
					a = a.split(";")
					T = a[0]
					P = a[1]
					H = a[2]
					D = a[3]
					newline += H+';'+T+';'+P+';'+D+'\n'
				newline = newline.strip()
				newline  = newline.split('\n')
				newli = ""
				for s in sorted(newline):
					newli += str(s)+"\n"
				newli = newli.split("\n")
				sinal = ""
				for index,a in enumerate(newli):
					if a == '':
						del newli[index]
				lista = ""
				for n in newli:
					n = n.split(";")
					T = n[1]
					P = n[2]
					H = n[0]
					D = n[3]
					sinal = T+';'+P+';'+H+';'+D
					lista += sinal+'\n'
					listt = lista.strip()
					tex = ""
					result = True
			return result, listt, tex
		except Exception as a:
			if 'nvalid literal fo' in str(a):
				a = 'Lista invalida'
			return False, '', str(a)
	
	def validate(date_text):
		try:
			if date_text != datetime.strptime(date_text, '%H:%M:%S').strftime('%H:%M:%S'):
				raise ValueError
			return True
		except ValueError:
			return False
	
	def validateD(date_text):
		try:
			if date_text != datetime.strptime(date_text, '%d/%m/%Y').strftime('%d/%m/%Y'):
				raise ValueError
			return True
		except ValueError:
			return False
	
	def dateTimeNowForString():
		data_e_hora_atuais = datetime.now()
		fuso_horario = timezone('America/Sao_Paulo')
		data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
		datetimeatual = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M:%S')
		return datetimeatual
	
class controlValue:
	def conf_(name):
		name = str(name)
		try:
			config = open(name+'.json', 'r').read()	
		except:
			config = open(name+'.json', 'w')
			config = open(name+'.json', 'r').read()
			pass
		config = json.loads(config)
				
		return config
	
	def conf(name,data = False):
		name = str(name)
		default = {
"user":False}

		try:
			config = open(name+'.json', 'r').read()	
		except:
			ssss = open(name+'.json', 'w')
			config = open(name+'.json', 'r').read()
			pass
		if config.strip() == '':
			with open(name+'.json', 'w') as old_config:
				json.dump(default, old_config, indent=1)

			config = default
		else:
			config = json.loads(config)

		if data != False:
			for conf in data:
				config[conf] = data[conf]

			with open(name+'.json', 'w') as old_config:
				json.dump(config, old_config, indent=1)

		else:
			return config
	def calc(Valor,r,ns,nivel,NivelSoros):
		if ns == 0:
			r = 'n'
		else:
			if ns <= int(NivelSoros):
				r = 'n'
				if ns == 1:
					if nivel == 1:
						investPct = Valor * 50.11 / 100 
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 90.00 / 100
						Valor =  round(float(investPct),2)
				elif ns == 2:
					if nivel == 1:
						investPct = Valor * 74.80 / 100
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 135.00 / 100
						Valor =  round(float(investPct),2)
				elif ns == 3:
					if nivel == 1:
						investPct = Valor * 187.30 / 100   
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 337.05/ 100   
						Valor =  round(float(investPct),2)
				elif ns == 4:
					if nivel == 1:
						investPct = Valor * 318.30 / 100   
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 573.00 / 100   
						Valor =  round(float(investPct),2)
				elif ns == 5:
					if nivel == 1:
						investPct = Valor * 571.00 / 100   
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 1027.60 / 100   
						Valor =  round(float(investPct),2)
				elif ns == 6:
					if nivel == 1:
						investPct = Valor * 1015.60 / 100   
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 1828.20 / 100   
						Valor =  round(float(investPct),2)
				elif ns == 7:
					if nivel == 1:
						investPct = Valor * 1808.90 / 100   
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 3255.90 / 100   
						Valor =  round(float(investPct),2)
				elif ns == 8:
					if nivel == 1:
						investPct = Valor * 3221.10 / 100   
						Valor =  round(float(investPct),2)
					elif nivel == 2:
						investPct = Valor * 5798.20 / 100   
						Valor =  round(float(investPct),2)
						ns = 0
			else:
				ns = 0
				nivel = 0
				r = "s"
		
		return Valor,r,ns,nivel
	
	def CalcSo(base):
		try:
			base =  round(float(base),2)
			entrada1 = base * 50.11 / 100 
			entrada1 =  round(float(entrada1),2)
			entrada15 = base * 90.00 / 100
			entrada15 =  round(float(entrada15),2)
			entrada2 = base * 74.80 / 100
			entrada2=  round(float(entrada2),2)
			entrada25 = base * 135.00 / 100
			entrada25 =  round(float(entrada25),2)
			entrada3 = base * 187.30 / 100   
			entrada3 =  round(float(entrada3),2)
			entrada35 = base * 337.05/ 100   
			entrada35 =  round(float(entrada35),2)
			entrada4 = base * 318.30 / 100   
			entrada4 =  round(float(entrada4),2)
			entrada45 = base * 573.00 / 100   
			entrada45 =  round(float(entrada45),2)
			entrada5 = base * 571.00 / 100   
			entrada5 =  round(float(entrada5),2)
			entrada55 = base * 1027.60 / 100   
			entrada55 =  round(float(entrada55),2)
			entrada6 = base * 1015.60 / 100   
			entrada6 =  round(float(entrada6),2)
			entrada65 = base * 1828.20 / 100   
			entrada65 =  round(float(entrada65),2)
			entrada7 = base * 1808.90 / 100   
			entrada7 =  round(float(entrada7),2)
			entrada75 = base * 3255.90 / 100   
			entrada75 =  round(float(entrada75),2)
			entrada8 = base * 3221.10 / 100   
			entrada8 =  round(float(entrada8),2)
			entrada85 = base * 5798.20 / 100   
			entrada85 =  round(float(entrada85),2)
			data = pd.DataFrame([
			  ['1º','R$'+str(base),    ],
			  ['1º','R$'+str(entrada1) ],
			  ['2º','R$'+str(entrada15)],
			  ['1º','R$'+str(entrada2) ],
			  ['2º','R$'+str(entrada25)],
			  ['1º','R$'+str(entrada3) ],
			  ['2º','R$'+str(entrada35)],
			  ['1º','R$'+str(entrada4) ],
			  ['2º','R$'+str(entrada45)],
			  ['1º','R$'+str(entrada5) ],
			  ['2º','R$'+str(entrada55)],
			  ['1º','R$'+str(entrada6) ],
			  ['2º','R$'+str(entrada65)],
			  ['1º','R$'+str(entrada7) ],
			  ['2º','R$'+str(entrada75)],
			  ['1º','R$'+str(entrada8) ],
			  ['2º','R$'+str(entrada85)],          
			], columns = ['',''], index=['INICIO', 'Nível  1', 'Nível  1', 'Nível  2', 'Nível  2', 'Nível  3', 'Nível  3'
			, 'Nível  4', 'Nível  4', 'Nível  5', 'Nível  5', 'Nível  6', 'Nível  6', 'Nível  7', 'Nível  7', 'Nível  8', 'Nível  8'])
			return str(data)
		except Exception as a:
			return str("ERRO: "+str(a))
	
	def CalcGal(base):
		try:
			if True:
				base =  round(float(base),2)	
				data = pd.DataFrame([
					  ["R$"+str(base)],
					  ["R$"+str(base * 2)],
					  ["R$"+str(base * 4)],
					  ["R$"+str(base * 8)],
					  ["R$"+str(base * 16)],
					  ["R$"+str(base * 32)],
				], columns = [''], index=['EN', 'G1', 'G2', 'G3', 'G4', 'G5'])
			return data
		except Exception as a:
			return 'ERRO: '+str(a)
	def CalcCi(base):
		try:
			base =  round(float(base),2)	
			data = pd.DataFrame([
				  [str(base)],
				  [str(base * 2)],
				  [str(base * 4)],
				  [str(base * 8)],
				  [str(base * 16)],
				  [str(base * 32)],
				  [str(base * 64)],
				  [str(base * 168)],
				  [str(base * 336)],
				  [str(base * 672)],
				  [str(base * 1344)],
				  [str(base * 2688)],
			], columns = [''], index=['E', 'G1', 'G2', 'Nível 1-E', 'Nível 1-G1', 'Nível 1-G2', 'Nível 2-E', 'Nível 2-G1', 'Nível 2-G2','Nível 3-E', 'Nível3-G1','Nível 3-G2'])
			return str(data)
		except Exception as a:
			return str(a)
	def jurosCom(banca,prcnt,days):
		dia = 0 
		total = 0
		strings = 'INICIAL R$'+str(round(banca,2))+'\nDIA      LUCRO      TOTAL  '
		for i in range(days):
			prctAtual = (banca * prcnt) / 100
			stopWin = float(prctAtual)    
			total = banca + stopWin
			dia += 1
			strings += '\n   '+str(dia)+'      R$'+str(round(stopWin,2))+'      R$'+str(round(total,2))+'  '
			banca = total
		return	strings