
from tradingview_ta import TA_Handler, Interval, Exchange
from iqoptionapi.constants import Activ
from Controller.controlDao import connectDao
import time
class Reg():
	def bb(x,API):
		ss = ''
		sf = ''
		for timeframe in ['1','5','15']:
			for par in Activ:
				stickCandle = API.get_candles(par, (int(timeframe) * 60), 150, time.time())
				ultimo = round(stickCandle[0]['close'], 4)
				primeiro = round(stickCandle[-1]['close'], 4)
				diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
				tendencia = "call" if ultimo < primeiro and diferenca > 0.01 else "put" if ultimo > primeiro and diferenca > 0.01 else False
				if timeframe =='1':
					tmf = Interval.INTERVAL_1_MINUTE
				elif timeframe  == '5':
					tmf = Interval.INTERVAL_5_MINUTES
				elif timeframe == '15':
					tmf = Interval.INTERVAL_15_MINUTES
				try:
					Handler = TA_Handler(symbol=par,screener="forex",exchange=Exchange.FOREX,interval=tmf)
					rec = Handler.get_analysis().summary
					rec  = rec["RECOMMENDATION"]
					if "STRONG" in  rec:
						if "SELL" in rec:
							ss += "M"+timeframe+":"+str(par)+":chevron-triple-down:VENDA FORTE"#, [1, 0, 0, 1],'VENDA FORTE')))
						else:
							ss += "M"+timeframe+":"+str(par)+":chevron-triple-up:COMPRA FORTE"
					elif "SELL" in rec:
						ss += "M"+timeframe+":"+str(par)+":chevron-down:VENDA"
					elif "BUY" in rec:
						ss += "M"+timeframe+":"+str(par)+":chevron-up:COMPRA"
					else:
						ss += "M"+timeframe+":"+str(par)+":rectangle-outline:NEUTRO"
				except Exception as a:
					ss += "M"+timeframe+":"+str(par)+":rectangle-outline:NEUTRO"
					pass
				if tendencia == "put":
					ss += ":DOWN\n"
				else:
					ss += ":UP\n"

		if ss != sf:
			sf = ss
			connectDao.merc(ss)
		time.sleep(60)