from datetime import datetime, timedelta
import time
from pytz import timezone
from iqoptionapi.constants import ACTIVES,ACTIVCATALAGVip
import threading,json, os,io
from Controller.controlImage import mpfpl
import mplfinance as mpf
import pandas as pd
from Controller.controlCatalog import MsgTo
from Controller.controlEnum import MENSAGE
import time,logging
from tradingview_ta import Interval,TA_Handler,Exchange

logger = logging.getLogger()
logger.disabled = True

class ControlCheck():
	def umero_for_databr(x, mins):
		x = datetime.strptime(x,'%d/%m/%Y %H:%M:%S')
		x = x + timedelta(hours=3)
		pred3 = x + timedelta(minutes=mins)
		data = pred3.strftime('%d/%m/%Y %H:%M:%S')
		return data
	def umero_for_databrto(x, mins):
		x = datetime.strptime(x,'%d/%m/%Y %H:%M:%S')
		pred3 = x + timedelta(minutes=mins)
		data = pred3.strftime('%d/%m/%Y %H:%M:%S')
		return data
	def tnumericos(data, mins):
		data = ControlCheck.umero_for_databr(data, mins)
		dtnumerico = time.mktime(datetime.strptime(data, "%d/%m/%Y %H:%M:%S").timetuple())
		return dtnumerico
	def tnumericosgale(data, mins):
		data = ControlCheck.umero_for_databrto(data, mins)
		
		return data
	def numero_for_databr(x):
		x = datetime.fromtimestamp(x)
		data_em_texto = x.strftime("%d/%m/%Y %H:%M:%S")
		return data_em_texto
	def dtnumericos(data):
		dtnumerico = time.mktime(datetime.strptime(data, "%d/%m/%Y %H:%M:%S").timetuple())
		return dtnumerico
	def validate(date_text):
		try:
			if date_text != datetime.strptime(date_text, '%d/%m/%Y').strftime('%d/%m/%Y'):
				raise ValueError
			return True
		except ValueError:
			return False
	def dataMenosU(data):
		data = datetime.strptime(data,'%d/%m/%Y')
		data = data - timedelta(days=1)
		data = str(data.strftime('%d/%m/%Y'))
		return data
		
	def check(API,API_TOKEN,idd,lista,gale,date,arqname):
		try:
			gale = gale
			listast = lista.split('x')
			for lista in listast:
				if lista != '':
					check, lista, reason = controlParameter.ValidaList(lista)
					if check:
						Lista = str(lista).split('\n')
						Listalen = len(Lista)
						ListaResult = ""
						loss = 0 
						win = 0
						doji = 0
						porcnt = 0
						total = 0
						for sinal in Lista:
							parameter = sinal.split(';')
							T = str(parameter[0])[1:]
							P = str(parameter[1])
							TT = int(T)*60
							data = date+" "+str(parameter[2])
							d = 0
							datas = ControlCheck.tnumericosgale(data, int(T)*int(gale))
							dtnumerico = ControlCheck.tnumericos(data, int(T)*int(gale))
							velas = API.get_candles(P, TT, int(gale)+1, dtnumerico)
							x = 0
							if  str(datas) < str(controlParameter.dateTimeNowForString()):
								for vela in velas:
									if str(parameter[3]).strip() == 'CALL' and vela['open'] < vela['close'] or str(parameter[3]).strip() == 'PUT' and vela['open'] > vela['close']:
										win += 1
										lucro  = 9
										if x > 0:
											if d > 0:
												ListaResult += sinal+"🔹"+str(d)+"✅G"+str(x)+"\n"
											else:
												ListaResult += sinal+"✅G"+str(x)+"\n"
											
										else:
											if d > 0:
												ListaResult += sinal+"🔹"+str(d)+"✅G"+str(d)+"\n"
											else:
												ListaResult += sinal+"✅"+"\n"
										break
									elif str(parameter[3]).strip() == 'CALL' and vela['open'] > vela['close'] or str(parameter[3]).strip() == 'PUT' and vela['open'] < vela['close']:
										p = 0
										x += 1
										if x == int(gale)+1:
											loss += 1
											if d > 0:
												ListaResult += sinal+"🔹"+str(d)+"\n"
											else:
												ListaResult += sinal+"🛑\n"
											break
									else:
										doji += 1
										d += 1
										if d == int(gale)+1 or x == int(gale)+1:
											ListaResult += sinal+"♦️"+str(x)+"🔹"+str(d)+"\n"
											break
							else:
								ListaResult += sinal+"⏱\n"
						total = win + loss
						if ListaResult != "":
							porcnt = win / total * 100 
						porcnt = round(porcnt, 2)
						text = 'Total: '+str(total)+'\nPlacar: ✅'+str(win)+' X '+str(loss)+'🛑 - 🔹'+str(doji)+'\n Assertividade: '+str(porcnt)+'% \n\n'
						
						if Listalen > 140:
							try:
								with io.open(arqname+'.txt', 'w', encoding="utf-8") as arquivo:
									arquivo.write(ListaResult+"\n"+text)
									arquivo.close()
								MsgTo.upload_file(arqname+'.txt',idd,API_TOKEN)
								os.remove(arqname+'.txt')
							except Exception as a: 
								pass
						else:
							MsgTo.send_msg(ListaResult,idd,API_TOKEN)
							MsgTo.send_msg(text,idd,API_TOKEN)
					else:
						MsgTo.send_msg(reason,idd,API_TOKEN)
		except ZeroDivisionError:
			text = 'ev-0\n\nTotal: '+str(total)+'\nPlacar: ✅0 X 0🛑\nAssertividade: 0% \n\n'
			MsgTo.send_msg(text,idd,API_TOKEN)
			pass
		except Exception as a:
			text = str(a)+'\n\nTotal: '+str(total)+'\nPlacar: ✅0 X 0🛑\nAssertividade: 0% \n\n - contato o erro ao suporte'
			MsgTo.send_msg(text,idd,API_TOKEN)
			pass
		

	
class controlParameter():
	def get_pares(API,timeF,pairs):
		pair = []
		P = ''
		t = 0
		for timeF in [1,5,15]:
			pares = {"pares":{
			      "digital":{
				  
			      },
			      "turbo":{
				  
			      },
			      "binary":{
				  
			      }
			   }
			}
				
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
							time.sleep(0.1)
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
						time.sleep(1)
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
	

	def minutesMais5(x):
		x = datetime.strptime(x,'%H:%M:%S')
		pred3 = x + timedelta(minutes=1)
		interval_input5 = pred3.strftime('%H:%M:%S')
		return interval_input5
	
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
	
	
	def timestamp_converter(x):
		hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%H:%M:%S'), '%H:%M:%S')
		datetimebr = str(hora - timedelta(hours=3))
		return datetimebr
	def Tendencia(API,par,timeframe,cand,idd,name,API_TOKEN):
		stickCandle = API.get_candles(par, (int(timeframe) * 60), int(cand), time.time())
		ultimo = round(stickCandle[0]['close'], 4)
		primeiro = round(stickCandle[-1]['close'], 4)
		diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
		tendencia = "call" if ultimo < primeiro and diferenca > 0.01 else "put" if ultimo > primeiro and diferenca > 0.01 else False
		if tendencia == "put":
			MsgTo.send_msg('🦁:{0}, pelas minas análises concluí o seguinte :\n⬇️🔴TENDÊNCIA DE BAIXA - {1}🔴⬇️\n🔵LINHA AZUL SMA-60\n🟡LINHA AMARELA SMA-20'.format(name,par),idd,API_TOKEN)
		else:
			MsgTo.send_msg('🦁:{0}, pelas minas análises concluí o seguinte :\n⬆️🟢TENDÊNCIA DE ALTA - {1}🟢⬆️\n🔵LINHA AZUL SMA-60\n🟡LINHA AMARELA SMA-20'.format(name,par),idd,API_TOKEN)
		if timeframe >= 1 and timeframe <= 3:
			tmf = Interval.INTERVAL_1_MINUTE
		elif timeframe >= 4 and timeframe <= 7:
			tmf = Interval.INTERVAL_5_MINUTES
		elif timeframe > 7 and  timeframe < 30:
			tmf = Interval.INTERVAL_15_MINUTES
		else:
			tmf  = Interval.INTERVAL_1_HOUR
		if "OTC" not in par:
			Handler = TA_Handler(symbol=par,screener="forex",exchange=Exchange.FOREX,interval=tmf)
			rec = Handler.get_analysis().summary
			rec  = rec["RECOMMENDATION"]
			if "STRONG" in  rec:
				if "SELL" in rec:
					MsgTo.send_msg('🦁:{0}, na minhas análise considero o seguinte\n🔽🔴🔴VENDA FORTE🔴🔴🔽'.format(name,par),idd,API_TOKEN)
				else:
					MsgTo.send_msg('🦁:{0}, na minhas análise considero o seguinte\n🔼🟢🟢COMPRA FORTE🟢🟢🔼'.format(name,par),idd,API_TOKEN)
			elif "SELL" in rec:
				MsgTo.send_msg('🦁:{0}, na minhas análise considero o seguinte\n🔽🔴VENDA🔴🔽'.format(name,par),idd,API_TOKEN)
			elif "BUY" in rec:
				MsgTo.send_msg('🦁:{0}, na minhas análise considero o seguinte\n🔼🟢COMPRA🟢🔼'.format(name,par),idd,API_TOKEN)
			else:
				MsgTo.send_msg('🦁:{0}, na minhas análise considero o seguinte\⏹⚪️NEUTRO⚪️⏹'.format(name,par),idd,API_TOKEN)
		mydic = dict()
		mydic['Date'] = []
		mydic['Open'] = []
		mydic['High'] = []
		mydic['Low'] = []
		mydic['Close'] = []
		mydic['Volume'] = []
		for vel in stickCandle:
			mydic['Date'].append(datetime.fromtimestamp(vel['from']))
			mydic['Open'].append(vel['open'])
			mydic['High'].append(vel['max'])
			mydic['Low'].append(vel['min'])
			mydic['Close'].append(vel['close'])
			mydic['Volume'].append(vel['volume'])
		data = pd.DataFrame.from_dict(mydic)
		data.set_index('Date', inplace=True)
		arqname = str(datetime.now())
		arqname = str(datetime.now())
		arqname = arqname.replace(".","")
		arqname = arqname.replace(" ","")
		arqname = arqname.replace(":","")
		arqname = arqname.replace("-","")
		arqname = name+arqname+'.png'
		mc = mpf.make_marketcolors(up='#00ff40',down='#ff0000',inherit=True)
		s  = mpf.make_mpf_style(base_mpf_style='yahoo',marketcolors=mc)
		width_config={'candle_linewidth':0.8, 'candle_width':0.525, 'volume_width': 0.525}
		min = stickCandle[0]['close']
		max = stickCandle[0]['close']
		for p in stickCandle:
			if p['close'] < min:
				min = p['close']
			if p['close']> max:
				max = p['close']
		threading.Thread(target=mpfpl, args=(mpf,width_config,max,min,s,arqname,data,stickCandle,par,timeframe,idd,API_TOKEN),daemon=True).start()
		

	
		
	def escrever_json(lista):
		with open('run.json', 'r') as f:
			line = json.load(f)
			line.append(lista)
		with open('run.json', 'w') as f:
			json.dump(line, f)

	def carregar_json():
		with open('run.json', 'r') as f:
			return json.load(f)

	def escrever_jsons(a):
		with open('run.json', 'w') as f:
			f.truncate()
			json.dump(a, f)

	def reescrever_json(a):
		with open('run.json', 'r') as f:
			line = json.load(f)
			line.remove(a)
		controlParameter.escrever_jsons(line)
	
	def escrever_jsonF(lista):
		with open('runFULL.json', 'r') as f:
			line = json.load(f)
			line.append(lista)
		with open('runFULL.json', 'w') as f:
			json.dump(line, f)

	def carregar_jsonF():
		with open('runFULL.json', 'r') as f:
			return json.load(f)

	def escrever_jsonsF(a):
		with open('runFULL.json', 'w') as f:
			f.truncate()
			json.dump(a, f)

	def reescrever_jsonF(a):
		with open('runFULL.json', 'r') as f:
			line = json.load(f)
			line.remove(a)
		controlParameter.escrever_jsonsF(line)
	def CalcularSo(base,Stw,Stl, balance):
		try:
			base = round(float(base),2)
			stopWin = (balance * Stw) / 100
			stopLoss = (balance * Stl) / 100
			stopWin = float(stopWin)    
			stopLoss = float(stopLoss)
			stopWin = balance + stopWin
			stopLoss = balance - stopLoss
			SlTxt = "-R$ "+str(round(stopLoss,2))
			SwTxt = "R$ "+str(round(stopWin,2))
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
			s = MENSAGE.MSG010.value.format(str(base),str(entrada1),str(entrada15),str(entrada2),str(entrada25),str(entrada3),str(entrada35),str(entrada4),str(entrada45),str(entrada5) ,str(entrada55),str(entrada6) ,str(entrada65),str(entrada7) ,str(entrada75),str(entrada8) ,str(entrada85),SwTxt,SlTxt,base)
			return s
		except Exception as a:
			pass
			return str(a)
	def CalcularCi(base,Stw,Stl,gale,factor,balance):
		
		base = round(float(base),2)
		stopWin = (balance * Stw) / 100
		stopLoss = (balance * Stl) / 100
		stopWin = float(stopWin)    
		stopLoss = float(stopLoss)
		stopWin = balance + stopWin
		stopLoss = balance - stopLoss
		SlTxt = "-R$ "+str(round(stopLoss,2))
		SwTxt = "R$ "+str(round(stopWin,2))

		if gale == 1:
			NIVEL1  = round(float(base),2)
			NIVEL15 = round(float(NIVEL1 * factor ),2) 
			NIVEL2  = round(float(NIVEL15 * factor),2)
			NIVEL25 = round(float(NIVEL2  * factor),2)	
			NIVEL3  = round(float(NIVEL25 * factor),2)
			NIVEL35 = round(float(NIVEL3  * factor),2)
			NIVEL4  = round(float(NIVEL35 * factor),2)
			NIVEL45 = round(float(NIVEL4  * factor),2)
			NIVEL5  = round(float(NIVEL45 * factor),2)
			NIVEL55 = round(float(NIVEL5  * factor),2)
			return MENSAGE.MSG011.value.format(base,NIVEL1,NIVEL15, NIVEL2, NIVEL25, NIVEL3,NIVEL35, NIVEL4, NIVEL45, NIVEL5, NIVEL55,SlTxt,SwTxt)
		elif gale == 2:
			NIVEL1  = round(float(base),2)
			NIVEL15 = round(float(NIVEL1 * factor),2) 
			NIVEL2  = round(float(NIVEL15 * factor),2)
			NIVEL25 = round(float(NIVEL2  * factor),2)
			NIVEL3  = round(float(NIVEL25 * factor),2)
			NIVEL35 = round(float(NIVEL3  * factor),2)
			NIVEL4  = round(float(NIVEL35 * factor),2)
			NIVEL45 = round(float(NIVEL4  * factor),2)
			NIVEL5  = round(float(NIVEL45 * factor),2)
			NIVEL55 = round(float(NIVEL5  * factor),2)
			NIVEL6  = round(float(NIVEL55 * factor),2)
			NIVEL65 = round(float(NIVEL6  * factor),2)
			NIVEL7  = round(float(NIVEL65 * factor),2)
			NIVEL75 = round(float(NIVEL7  * factor),2)
			NIVEL8 =  round(float(NIVEL75  * factor),2)
			NIVEL85  = round(float(NIVEL8 * factor),2)
			NIVEL9 = round(float(NIVEL85  * factor),2)
			NIVEL95 =  round(float(NIVEL9  * factor),2)
			return MENSAGE.MSG012.value.format(base,NIVEL1,NIVEL15, NIVEL2, NIVEL25, NIVEL3,NIVEL35, NIVEL4,NIVEL45, NIVEL5, NIVEL55,NIVEL6,NIVEL65,NIVEL7,NIVEL75,NIVEL8,NIVEL85,NIVEL9,NIVEL95,SlTxt,SwTxt)
		else:
			NIVEL1  = round(float(base),2)
			NIVEL2 = round(float(NIVEL1 * factor ),2) 
			NIVEL3  = round(float(NIVEL2 * factor),2)
			NIVEL4 = round(float(NIVEL3  * factor),2)	
			NIVEL5  = round(float(NIVEL4 * factor),2)
			NIVEL6 = round(float(NIVEL5  * factor),2)
			return MENSAGE.MSG013.value.format(base,NIVEL1,NIVEL2, NIVEL3, NIVEL4, NIVEL5, SlTxt,SwTxt)
			
			a = 0

		base = round(float(base),2)
	
	def Calcular(typeacc,stopWinPct,investPct,stopLossPct, balance):
		stopWin = (balance * stopWinPct) / 100
		stopLoss = (balance * stopLossPct) / 100
		stopWin = float(stopWin)    
		stopLoss = float(stopLoss)
		stopWin = balance + stopWin
		stopLoss = balance - stopLoss
		entrada = (balance * float(investPct)) / 100
		stl = "<span style='color:red'>🔴S.LOSS: R$"+str(round(stopLoss,2))+"</span>"
		stw = "<span style='color:lime'>🟢S.WIN: R$"+str(round(stopWin,2))+"</span>"
		enter = "<span style='color:white'>⚪️INVESTIR: R$"+str(round(entrada,2))+"</span>"
		return stl, stw,enter
	def balancePr(API):
		global bid
		API.change_balance('PRACTICE')
		balancePrt = API.get_balance()
		balancePrt = round(float(balancePrt),2)
		bid = balancePrt
		return balancePrt
	def balanceRl(API):
		global bir
		API.change_balance('REAL')
		balanceRl = API.get_balance()
		balanceRl = round(float(balanceRl),2)
		bir = balanceRl
		return balanceRl
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
					tex = 'Lista: Tempo não permitido! set - "'+str(T)+'"'
					listt = []
					result = False
				elif P not in ACTIVES:
					tex = 'Lista: Par não existe! set - "'+P+'"'
					listt = []
					result = False
				elif controlParameter.validate(H) == False:
					tex = 'Lista: Horario não existe! set - "'+H+'"'
					listt = []
					result = False
				elif D != "CALL" and D != "PUT":
					tex = 'Lista: Erro na Paridade! set = "'+D+'"'
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
			lista = lista.replace(' ',"\n")
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
					tex = 'Lista: Tempo não permitido! set - "'+str(T)+'" Digite /helpList'
					listt = []
					result = False
				elif P not in ACTIVES:
					tex = 'Lista: Par não existe! set - "'+P+'" Digite /helpList'
					listt = []
					result = False
				elif controlParameter.validate(H) == False:
					tex = 'Lista: Horario não existe! set - "'+H+'" Digite /helpList'
					listt = []
					result = False
				elif D != "CALL" and D != "PUT":
					tex = 'Lista: Erro na Paridade! set = "'+D+'" Digite /helpList'
					listt = []
					result = False
			if listt != []:
				newline = ""
				for a in configli:
					if a != '':
						a = a.split(";")
						T = a[0].strip()
						P = a[1].strip()
						H = a[2].strip()
						D = a[3].strip()
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
			elif "EUS SINAIS NO CAMPO DE TEXTO E ENV" in str(a):
				a = 'use uma lista não aperta o botão'
			return False, '', str(a)
class controlValue:	
	
	def calc(Valor,r,ns,nivel,NivelSoros):
		if ns == 0:
			r = 'n'
		else:
			if ns <= int(8):
				r = 'n'
				if ns == 1:
					if nivel == 1:
						entrada = Valor * 50.11 / 100 
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 90.00 / 100
						Valor =  round(float(entrada),2)
				elif ns == 2:
					if nivel == 1:
						entrada = Valor * 74.80 / 100
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 135.00 / 100
						Valor =  round(float(entrada),2)
				elif ns == 3:
					if nivel == 1:
						entrada = Valor * 187.30 / 100   
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 337.05/ 100   
						Valor =  round(float(entrada),2)
				elif ns == 4:
					if nivel == 1:
						entrada = Valor * 318.30 / 100   
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 573.00 / 100   
						Valor =  round(float(entrada),2)
				elif ns == 5:
					if nivel == 1:
						entrada = Valor * 571.00 / 100   
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 1027.60 / 100   
						Valor =  round(float(entrada),2)
				elif ns == 6:
					if nivel == 1:
						entrada = Valor * 1015.60 / 100   
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 1828.20 / 100   
						Valor =  round(float(entrada),2)
				elif ns == 7:
					if nivel == 1:
						entrada = Valor * 1808.90 / 100   
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 3255.90 / 100   
						Valor =  round(float(entrada),2)
				elif ns == 8:
					if nivel == 1:
						entrada = Valor * 3221.10 / 100   
						Valor =  round(float(entrada),2)
					elif nivel == 2:
						entrada = Valor * 5798.20 / 100   
						Valor =  round(float(entrada),2)
						ns = 0
			else:
				ns = 0
				nivel = 0
				r = "s"
		
		return Valor,r,ns,nivel
	
	def StopLoWi(API, stopLoss,stopWin,balance):
		Stop = False
		text = ''
		stopWin = (balance * stopWin) / 100
		stopLoss = (balance * stopLoss) / 100
		stopWin = float(stopWin)    
		stopLoss = float(stopLoss)
		stopWin = balance + stopWin
		stopLoss = balance - stopLoss
		BalanceNow = API.get_balance()
		BalanceNow = float(BalanceNow)	
		StopWin = (BalanceNow >= stopWin)
		StopLoss = (BalanceNow <= stopLoss)
		LuPe = BalanceNow - balance
		LuPe = str(round(LuPe, 2))
		if StopWin:
			Stop = True
			text = ' STOP WIN !☞ R$'+LuPe+''
		elif StopLoss:
			Stop = True
			text =  'STOP LOSS !☞ R$'+LuPe+''
		return Stop, text
		

	def minutesMais5(x):
		x = datetime.strptime(x,'%H:%M:%S')
		pred3 = x + timedelta(minutes=1)
		interval_input5 = pred3.strftime('%H:%M:%S')
		return interval_input5
	
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
	
	def delay_input(x,y):
		x = datetime.strptime(x,'%d/%m/%Y %H:%M:%S')
		pred3 = x - timedelta(seconds=y)
		interval_input5 = pred3.strftime('%d/%m/%Y %H:%M:%S')
		return interval_input5
	
	def timestamp_converter(x):
		hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%H:%M:%S'), '%H:%M:%S')
		datetimebr = str(hora - timedelta(hours=3))
		return datetimebr
	
	def visutrend(par,direction,tendencia,idd,telegramTk):
		if tendencia == "call":
			text = '<b>••••••••••••••AVISO•••••••••••\n••••••••••••••••••••••••••••••••••\n<i>&#x1f916;:  ☞Tendencia: ALTA - Direção:'+direction.upper()+' - &#x1f4b9;  ' + par + ' </i>\n••••••••••••••••••••••••••••••••••</b>'
			MsgTo.send_msg(text, idd,telegramTk)
		else:
			text = '<b>••••••••••••••AVISO•••••••••••\n••••••••••••••••••••••••••••••••••\n<i>&#x1f916;:  ☞Tendencia: BAIXA - Direção:'+direction.upper()+' - &#x1f4b9;  ' + par + ' </i>\n••••••••••••••••••••••••••••••••••</b>'
			MsgTo.send_msg(text, idd,telegramTk)
	
	def interval_input5(x):
		x = datetime.strptime(x,'%d/%m/%Y %H:%M:%S')
		pred3 = x + timedelta(seconds=2)
		interval_input5 = pred3.strftime('%d/%m/%Y %H:%M:%S')
		return interval_input5
	
	def Tendencia(par,timeframe,direction, API,idd,telegramTk):
		velas = API.get_candles(par, (int(timeframe) * 60), 20, time.time())
		ultimo = round(velas[0]['close'], 4)
		primeiro = round(velas[-1]['close'], 4)
		diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
		tendencia = "call" if ultimo < primeiro and diferenca > 0.01 else "put" if ultimo > primeiro and diferenca > 0.01 else False
		if tendencia == False:
			tendencia = direction
		threading.Thread(target=controlParameter.visutrend, args=(par,direction,tendencia,idd,telegramTk),daemon=True).start()
		return tendencia
	
	def escrever_json(lista):
		with open('run.json', 'r') as f:
			line = json.load(f)
			line.append(lista)
		with open('run.json', 'w') as f:
			json.dump(line, f)

	def carregar_json():
		with open('run.json', 'r') as f:
			return json.load(f)

	def escrever_jsons(a):
		with open('run.json', 'w') as f:
			f.truncate()
			json.dump(a, f)

	def reescrever_json(a):
		with open('run.json', 'r') as f:
			line = json.load(f)
			line.remove(a)
		controlParameter.escrever_jsons(line)
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
		
