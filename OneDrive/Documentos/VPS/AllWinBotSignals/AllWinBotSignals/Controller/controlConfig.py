from Controller.message import controlMessage


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
	
class controlValue:
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
	
	def StopLoWi(API, stopLoss,stopWin, idd, balance,telegramTk):
		Stop = False
		r =''
		BalanceNow = API.get_balance()
		BalanceNow = float(BalanceNow)	
		StopWin = (BalanceNow >= stopWin)
		StopLoss = (BalanceNow <= stopLoss)
		LuPe = BalanceNow - balance
		LuPe = str(round(LuPe, 2))
		if StopWin:
			Stop = True
			r = 'W'
			text = '&#x1f916;:  STOP WIN ATIGINDO! R$'+LuPe+'⚠️ AS ORDENS QUE ESTOU RODANDO AGORA PODEM ATINGIR O STOP WIN , AGUARDE O RESULTADO.'
			controlMessage.send_msg(text, idd,telegramTk)  
		elif StopLoss:
			Stop = True
			r = 'L'
			text = '&#x1f916;:  STOP LOSS ATIGINDO! R$'+LuPe+'\n ⚠️ AS ORDENS QUE ESTOU RODANDO AGORA PODEM ATINGIR O STOP LOSS , AGUARDE O RESULTADO.'
			controlMessage.send_msg(text, idd,telegramTk) 
		return Stop,r
	
	def Stopvery(API, stopLoss,stopWin, idd, balance,telegramTk):
		Stop = False
		BalanceNow = API.get_balance()
		BalanceNow = float(BalanceNow)	
		StopWin = (BalanceNow >= stopWin)
		StopLoss = (BalanceNow <= stopLoss)
		LuPe = BalanceNow - balance
		LuPe = str(round(LuPe, 2))
		if StopWin:
			Stop = True
		elif StopLoss:
			Stop = True
		return Stop
	def StopLo(API, stopLoss,stopWin, idd, balance,telegramTk):
		Stop = False
		BalanceNow = API.get_balance()
		BalanceNow = float(BalanceNow)	
		StopLoss = (BalanceNow <= stopLoss)
		if StopLoss:
			Stop = True
		return Stop
	def StopWi(API, stopLoss,stopWin, idd, balance,telegramTk):
		Stop = False
		BalanceNow = API.get_balance()
		BalanceNow = float(BalanceNow)	
		StopWin = (BalanceNow >= stopWin)
		if StopWin:
			Stop = True
		return Stop
