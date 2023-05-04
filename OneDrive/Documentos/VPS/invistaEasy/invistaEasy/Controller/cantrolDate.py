import time, logging
from datetime import datetime, timedelta
from pytz import timezone
logger = logging.getLogger()
logger.disabled = True

def umero_for_databr(x, mins):
	x = datetime.strptime(x,'%d/%m/%Y')
	pred3 = x + timedelta(minutes=mins)
	interval_input5 = pred3.strftime('%d/%m/%Y')
	return interval_input5
def tnumericos(data, mins):
	data = umero_for_databr(data, mins)
	dtnumerico = time.mktime(datetime.strptime(data, "%d/%m/%Y").timetuple())
	return dtnumerico
def dateTimeNowFordate():
	data_e_hora_atuais = datetime.now()
	fuso_horario = timezone('America/Sao_Paulo')
	data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
	return data_e_hora_sao_paulo
def dateTimeNowForString():
	data_e_hora_atuais = datetime.now()
	fuso_horario = timezone('America/Sao_Paulo')
	data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
	datetimeatual = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M:%S')
	return datetimeatual
	