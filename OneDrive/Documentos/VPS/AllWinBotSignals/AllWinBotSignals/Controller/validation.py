from datetime import datetime
from Controller.fileSettings import file
from iqoptionapi.constants import ACTIVES
from iqoptionapi.stable_api import IQ_Option
from Controller.controlDao import connectDao
import os,time

class validate:
	def hours(hours_text):
		try:
			if hours_text != datetime.strptime(hours_text, '%H:%M:%S').strftime('%H:%M:%S'):
				raise ValueError
			return True
		except ValueError:
			return False
	def is_number(d):
		try:
			float(d)
			return d
		except ValueError:
			return False
		except TypeError:
			return False
	def is_param(d):
		try:
			if d in ["1","2","3","4","5","6","7","8","9","10",
				"11","12","13","14","15","16","17","18","19",
				"20","21","22","23","24","25","26","27","28","29",
				"30","31","32","33","34","35","36","37","38","39",
				"40","41","42","43","44","45","46","47","48","49",
				"50","51","52","53","54","55","56","57","58","59",
				"60","61","62","63","64","65","66","67","68","69",
				"70","71","72","73","74","75","76","77","78","79",
				"80","81","82","83","84","85","86","87","88","89",
				"90","91","92","93","94","95","96","97","98","99","Cancelar",'OK','SIM','NÃO']:
				return d
			else:
				float(d)
				return d
		except ValueError:
			return False
		except TypeError:
			return False
	def listSigns(lista):
		try:
			if len(lista.split('\n')) >= 170:
				return False
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
					listt = []
					return False
				elif P not in ACTIVES:
					listt = []
					return False
				elif validate.hours(H) == False:
					listt = []
					return False
				elif D != "CALL" and D != "PUT":
					listt = []
					return False
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

	def datailsListSigns(lista):
		try:
			if len(lista.split('\n')) >= 170:
				return False, [], 'Lista muito grande. Quantidade: '+str(len(lista.split('\n')))+" - Limite: 170"
			tex = ''
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
				elif validate.hours(H) == False:
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
					result = True
			return result, listt, tex
		except Exception as a:
			if 'nvalid literal fo' in str(a):
				a = 'Lista invalida'
			return False, '', str(a)
	def verify(API,email, passw,accT):
		T = True
		con = 0
		while T:
			try:
				con += 1
				API = IQ_Option(email, passw)
				API.connect()
				if API.check_connect():
					API.change_balance("REAL" if accT == "REAL" else "PRACTICE")
					T = False
					return  API	
				else:
					time.sleep(10)
				if con == 5:
					T = False
					return  API		
			except:
				time.sleep(10)
				if con == 5:
					T = False
					return  API
				pass									
	def verifyIQ(email, passwd,idUser,Key,passwdF):
		try:
		#if True:
			Check = True
			if Check == True:
				#API.change_balance("PRACTICE")
				if  0 == 0:
					if os.path.isfile(idUser+".txt"):
						file.alterParameter(idUser,'email',email)
						file.alterParameter(idUser,'valid',True)
						file.alterParameter(idUser,'passwd',passwdF)
						file.alterParameter(idUser,'key',Key)
					else:
						file.create(idUser)
						file.alterParameter(idUser,'email',email)
						file.alterParameter(idUser,'passwd',passwdF)
						file.alterParameter(idUser,'key',Key)
						file.alterParameter(idUser,'valid',True)
				else:
					if os.path.isfile(idUser+".txt"):
						file.alterParameter(idUser,'email',email)
						file.alterParameter(idUser,'valid',True)
						file.alterParameter(idUser,'passwd',passwdF)
						file.alterParameter(idUser,'key',Key)
					else:
						file.create(idUser)
						file.alterParameter(idUser,'email',email)
						file.alterParameter(idUser,'passwd',passwdF)
						file.alterParameter(idUser,'key',Key)
						file.alterParameter(idUser,'valid',False)
			else:
				if os.path.isfile(idUser+".txt"):
					file.alterParameter(idUser,'email',False)
					file.alterParameter(idUser,'passwd',False)
					file.alterParameter(idUser,'valid',False)
					file.alterParameter(idUser,'key',False)
				else:
					file.create(idUser)
					file.alterParameter(idUser,'email',False)
					file.alterParameter(idUser,'passwd',False)
					file.alterParameter(idUser,'key',False)
					file.alterParameter(idUser,'valid',False)

		except Exception as a:
			if os.path.isfile(idUser+".txt"):
				file.alterParameter(idUser,'email',False)
				file.alterParameter(idUser,'passwd',False)
				file.alterParameter(idUser,'valid',False)
				file.alterParameter(idUser,'key',False)
			else:
				file.create(idUser)
				file.alterParameter(idUser,'email',False)
				file.alterParameter(idUser,'passwd',False)
				file.alterParameter(idUser,'key',False)
				file.alterParameter(idUser,'valid',False)
			pass