import telegram
from telegram import ParseMode
from Controller.datesTimes import hour

class controlMessage:
	def	AttSis(API, stopWin, stopLoss,telegramTk, balance,name,idd,nmeLista):
		try:
			BalanceNow = API.get_balance()
			BalanceNow = float(BalanceNow)	
			LuPe = BalanceNow - balance
			LuPe = str(round(LuPe, 2))
			text='&#x1f916;: '+name+', \nLucro/Prejuizo: '+LuPe+' - '+nmeLista+'\n'
			controlMessage.send_msg(text, idd,telegramTk)
		except Exception as a:
			text='&#x1f916;: Erro: '+str(a)
			controlMessage.send_msg(text, idd,telegramTk)
			pass
	def send_msg(texto, idd,telegramTk):
		try:
			if telegramTk != None:
				bot = telegram.Bot(token=telegramTk)
				bot.sendMessage(parse_mode=ParseMode.HTML, chat_id=idd, text='' + texto + '')
		except Exception as a:
			if 'Chat not found' not in str(a) or 'bot was blocked by the user' not in str(a):
				controlMessage.send_msg("class controll def send_msg"+str(idd)+" ALLWINTEL "+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
			pass
	def sendWinOrLossOrDoji(API,name, Par, lucro, Val,Time, type,balance, idd, investPct, gale,investPctf,pOut,telegramTk,dir, notfy,msg4):
		if 'Cannot purchase an option (active is suspended)' in str(notfy) or 'invalid instrument' in str(notfy) or 'active_suspended' in str(notfy) or 'active_closed' in str(notfy):
			notfy = 'Ativo Fechado'
		elif "Payout" in str(notfy):
			notfy = "Payout abaixo do especificado"
		elif 'amount must be positive' in str(notfy):
			notfy = 'Valor não positivo - Investido: R$'+str(Val)
		else:
			notfy = "Ordem Bloqueada"
		BalanceNow = API.get_balance()
		BalanceNow = float(BalanceNow)
		LuPe = BalanceNow - balance
		LuPe = str(round(LuPe, 2))
		if float(LuPe) > 0:
			LP = "🤑"
			
		else:
			LuPe = abs(float(LuPe))
			LP = "😨-"
		galin = '<sup>'+str(gale)+'</sup>'
		if type == "biw" or type == "diw":
			if 'b' in  type:
				investPctf = str(hour.timestamp_converter(investPctf))[11:-3]
			else:
				investPctf = hour.timestamp_converter(int(investPctf))[11:-3]
			res = round(lucro,2)
			text="📊 M"+str(Time)+":"+Par+":"+str(investPctf)+":"+str(dir.upper())+" ✅\n\n🤩 Payout: "+pOut[1:]+"%\n\n💸 Resultado da ordem: +R$"+str(res)+'\n\n'+LP+'  R$' + str(LuPe)+ '\n\n'+'💰 R$'+str(round(BalanceNow,2))
		elif type == "biwg" or type == "diwg":
			if 'b' in  type:
				investPctf = str(hour.timestamp_converter(investPctf))[11:-3]
			else:
				investPctf = hour.timestamp_converter(int(investPctf))[11:-3]
			res = round(lucro,2)
			text="📊 M"+str(Time)+":"+Par+":"+str(investPctf)+":"+str(dir.upper())+" ✅<i>G"+str(gale)+"</i>\n\n🤩 Payout: "+pOut[1:]+"%\n\n💸 Resultado da ordem: +R$"+str(res)+'\n\n'+LP+'  R$' + str(LuPe)+ '\n\n'+'💰 R$'+str(round(BalanceNow,2))
		elif type == "bil" or type == "dil":
			if 'b' in  type:
				investPctf = str(hour.timestamp_converter(investPctf))[11:-3]
			else:
				investPctf = hour.timestamp_converter(int(investPctf))[11:-3]
			res = abs(round(float(lucro),2))
			text  = "📊 M"+str(Time)+":"+Par+":"+str(investPctf)+":"+str(dir.upper())+" ✖️\n\n⭕️ Resultado da ordem: -R$"+str(res)+'\n\n'+LP+'  R$' + str(LuPe)+ '\n\n'+'💰 R$'+str(round(BalanceNow,2))
		elif type == "bilg" or type == "dilg":
			if 'b' in  type:
				investPctf = str(hour.timestamp_converter(investPctf))[11:-3] 
			else:
				investPctf = hour.timestamp_converter(int(investPctf))[11:-3]
			res = abs(round(float(lucro),2))
			text  = "📊 M"+str(Time)+":"+Par+":"+str(investPctf)+":"+str(dir.upper())+" ✖️<i>G"+str(gale)+"</i>\n\n⭕️ Resultado da ordem: -R$"+str(res)+'\n\n'+LP+'  R$' + str(LuPe)+ '\n\n'+'💰 R$'+str(round(BalanceNow,2))
		elif type == "die" or type == "bie":
			if 'b' in  type:
				investPctf = str(hour.timestamp_converter(investPctf))[11:-3]
			else:
				investPctf = hour.timestamp_converter(int(investPctf))[11:-3]
			res = abs(round(float(lucro),2))
			text = "📊 M"+str(Time)+":"+Par+":"+str(investPctf)+":"+str(dir.upper())+":DOJI\n\n⭕️Resultado da ordem: -R$"+str(res)+'\n\n'+LP+'  R$' + str(LuPe)+ '\n\n'+'💰 R$'+str(round(BalanceNow,2))
		elif type == "dieg" or type == "bieg":
			if 'b' in  type:
				investPctf = str(hour.timestamp_converter(investPctf))[11:-3]
			else:
				investPctf = hour.timestamp_converter(int(investPctf))[11:-3]
			res = abs(round(float(lucro),2))
			text = "📊 M"+str(Time)+":"+Par+":"+str(investPctf)+":"+str(dir.upper())+":DOJI<i> G"+str(gale)+"</i>\n\n⭕️Resultado da ordem: -R$"+str(res)+'\n\n'+LP+'  R$' + str(LuPe)+ '\n\n'+'💰 R$'+str(round(BalanceNow,2))
		elif type == "fod" or type == "fob":
			text = "📊 M"+str(Time)+":"+Par+":"+str(investPct)[:-3]+":"+str(dir.upper())+"\n\n⚠️ A ORDEM FOI BLOQUEADA PELA CORRETORA\n\n"+str(notfy)
		controlMessage.send_msg(text, idd, telegramTk)