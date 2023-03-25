from datetime import datetime, timedelta
from pytz import timezone
from dateutil import tz

class date:
	def currentDateString():
		data_e_hora_atuais = datetime.now()
		fuso_horario = timezone('America/Sao_Paulo')
		data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
		datetimeatual = data_e_hora_sao_paulo.strftime('%d/%m/%Y')
		return datetimeatual
	def dateTomorrowString():
		data_e_hora_atuais = datetime.now()
		data_e_hora_atuais = data_e_hora_atuais + timedelta(days=1)
		fuso_horario = timezone('America/Sao_Paulo')
		data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
		datetimeatual = data_e_hora_sao_paulo.strftime('%d/%m/%Y')
		return datetimeatual
	def dateDaysMore(daysMore):
		data_e_hora_atuais = datetime.now()
		data_e_hora_atuais = data_e_hora_atuais + timedelta(days=daysMore)
		fuso_horario = timezone('America/Sao_Paulo')
		data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
		datetimeatual = data_e_hora_sao_paulo.strftime('%d/%m/%Y')
		return datetimeatual

class hour:
	def currentSecondsString():
		data_e_hora_atuais = datetime.now()
		fuso_horario = timezone('America/Sao_Paulo')
		data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
		datetimeatual = data_e_hora_sao_paulo.strftime('%S')
		return datetimeatual
	def timestamp_converter(x):
		hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%H:%M:%S'), '%H:%M:%S')
		datetimebr = str(hora - timedelta(hours=3))
		return datetimebr
class dateHours:
	def intervalSeconds(x):
		x = datetime.strptime(x,'%d/%m/%Y %H:%M:%S')
		pred3 = x + timedelta(seconds=3)
		interval_input5 = pred3.strftime('%d/%m/%Y %H:%M:%S')
		return interval_input5
	def timestamp_converter():
		hora = datetime.now()
		tm = tz.gettz('America/Sao Paulo')
		hora_atual = hora.astimezone(tm)
		return hora_atual.strftime('%H:%M:%S')
	def dateTimeNowForString():
		data_e_hora_atuais = datetime.now()
		fuso_horario = timezone('America/Sao_Paulo')
		data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
		datetimeatual = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M:%S')
		return datetimeatual
