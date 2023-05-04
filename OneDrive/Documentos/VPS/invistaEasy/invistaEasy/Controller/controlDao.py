
from Controller.controlConfig import controlParameter
from cryptography.fernet import Fernet
import mysql.connector
from Controller.controlEnum import MENSAGE
import logging
logger = logging.getLogger()
logger.disabled = True
class connectDao:
	def selectIds(id):
		try:
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT * FROM copytraderone.chat_ids where name = 'easy' and ids = '"+id+"'")
			account = myCursor.fetchone()
			MyDb.close()
			if account == None:
				return True, None
			else: 
				return False, account
		except Exception as a:
			MyDb.close()
			return True, None
	def registeIrd(id):
			try:
				MyDb = connection.connection()
				myCursor = MyDb.cursor()
				myCursor.execute("INSERT INTO copytraderone.chat_ids (name, ids, data) VALUES ('one', '"+id+"', '"+str(controlParameter.dateTimeNowForString())+"');")
				MyDb.commit()
				myCursor.close()
				MyDb.close()
				return True,''
			except Exception as a:
				MyDb.close()
				return False,"ERRO: "+str(a)
	def insertAcc(idd, data):
			try:
				det = idd.split(',')
				chatId = det[0]
				name = det[1]
				MyDb = connection.connection()
				myCursor = MyDb.cursor()
				myCursor.execute("SELECT * FROM copytraderone.garratradingacc where chatId='"+chatId+"'")
				account = myCursor.fetchone()
				if account == None:
					myCursor = MyDb.cursor()
					myCursor.execute("INSERT INTO copytraderone.garratradingacc (name, chatId, active, type, sls) VALUES ('"+name+"', '"+chatId+"', '"+data+"', 'T', 'vip');")
					MyDb.commit()
					MyDb.close()
					return True,''
				else:
					MyDb.close()
					return False,"JÁ CADASTRADO"
			except Exception as a:
				MyDb.close()
				return False,"ERRO: "+str(a)
	def getParesBd():
		try:
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.pares")
			account = myCursor.fetchone()
			MyDb.close()
			if account == None:
				return False, None
			else: 
				return True, account[1].split(',')
				
		except Exception as a:
			MyDb.close()
			return False, None
	def AuthId(userId):
		try:
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT * FROM copytraderone.garratradingacc where chatId = '"+str(userId)+"' and active is not null")
			account = myCursor.fetchone()
			return True
		except Exception as a:
			#print(a)
			return True
	def merc(lista):
		MyDb = connection.connection()
		myCursor = MyDb.cursor()
		myCursor.execute('UPDATE copytraderone.listamerc SET  lista = "'+lista+'" where id = 1')
		MyDb.commit()
	def selectStart(idsecret,cod,idfk):
		MyDb = connection.connection()
		myCursor = MyDb.cursor()
		myCursor.execute("SELECT * FROM copytraderone.garraaccconfig where cod = '"+cod+"' and idsecret = '"+idsecret+"' and idfk = "+str(idfk)+"")
		config = myCursor.fetchone()
		if config == None:
			return False,None,None,None,None,None,None,None,None,None,None,None,None,None,None, 'Erro no token - contate o suporte🙄🙄'
		else: 
			if config[12] < str(controlParameter.dateTimeNowForString())[:10]:
				return False, None,None,None,None,None,None,None,None,None,None,None,None,None,'Lista desatualizada, vai operar no passado? não sou maquina do tempo brô😒🙄'
			else:			
				return True, config[4],config[5],config[6],config[7],config[8],config[9],config[10],config[11],config[12],config[13],config[14],config[15],config[16],config[17],'ok'
	
	def selectList(lista,typs):
		try:
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.garratradinsinais where typs = '"+typs+"' and type = '"+lista+"'")
			sinais = myCursor.fetchone()
			if sinais == None:
				return False, None, None, None, None, None, MENSAGE.MSG014.value
			else: 
				if sinais[3] < str(controlParameter.dateTimeNowForString())[:10]:
					return False, None, None, None, None, None,MENSAGE.MSG014.value
				else:
					return True, sinais[1],sinais[2],sinais[3],sinais[4],sinais[5],'ok'
		except Exception as a:
			return False, None, None, None, None, None, str(a)
			pass
	def UpdateConta(email, passwd, idd):
		try:
			key = Fernet.generate_key()
			f = Fernet(key)
			passwd = str(f.encrypt(bytes(passwd, 'utf-8')))
			passwd = str(passwd[2:-1])
			Key = str(key)
			Key = str(Key[2:-1])
			cod = str(Key[19:-19])
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.garratradingacc where email = '"+str(email)+"' and active is not null")
			myConta = myCursor.fetchone()
			if myConta != None:
				myCursor.execute("update copytraderone.garratradingacc set chatId = '"+str(idd)+"', tokenTelegram = '"+str(cod)+"', passwd = '"+passwd+"', keyPasswd = '"+Key+"' where email = '"+str(email)+"'")
				MyDb.commit()
				return True, cod
			else:
				return False, ''
		except Exception as a:
			pass
			return False, str(a)
	def updateStrategy(pair,time,filtro,syss,pct,sistema):
		try:
			MyDb2 = connection.connection()
			myCursor = MyDb2.cursor()
			myCursor.execute("SELECT * FROM copytraderone.strategy where par = '"+str(pair)+"' and time = '"+str(time)+"' and gale = '"+str(filtro)+"' and estrategia = '"+str(syss)+"' and pct >= '"+str(pct)+"'")
			account = myCursor.fetchone()
			MyDb2.close()
			if account != None:
				a = account[2].split('\n')
				i = 0
				resul = ''
				for det in a:
					if i == 0:
						det = "🔰"+sistema+"🔰"
					elif i == 4:
						det = det.replace("em","-")
					elif  '🟥' in det or '🟨' in det  or '🟩' in det or '🟧' in det:
						det = det+'\n'
					elif i == 6:
						det = det.replace("🔮","Assertividade: ")
						det = det.replace("de Acertos","")
					else:
						if det == '':
							det = '\n\n'
					resul += det
					i+=1
				resul = resul.replace("🔽","")
				resul = resul.replace("\n\nPróxima Entrada:","")
				resul = resul.replace("\nÚltimo Quadrante:","Última análise:")
				resul = resul.replace("Consecutivos:","sucessivos:")
				resul = resul.replace("🔮 ","")
				resul = resul.replace("Como operar? /help","")
				resul = resul.replace("\n🟩:","🟩:")
				
				return True, resul
			else: 
				return False,"Porcentagem abaixo de "+str(pct)+"%"
		except Exception as e:
			#print(e)
			return False,str(e)
	def UpdateConfig(idUser, cod, investPct, stopLossPct, stopWinPct, gale, factorGale, factorCiclos, operateOpt, signals, dateOp, trend, cons, typSratg, nivel,typeAcc):
		try:
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			dateOp = str(dateOp).split("-")
			dateOp = str(dateOp[2])+"/"+str(dateOp[1])+"/"+str(dateOp[0])
			myCursor.execute('UPDATE copytraderone.garraaccconfig SET  investPct = "'+investPct+'", stopLossPct = "'+stopLossPct+'", stopWinPct = "'+stopWinPct+'", gale = "'+gale+'", factorGale = "'+factorGale+'", factorCiclos = "'+factorCiclos+'", operateOpt = "'+operateOpt+'", signals = "'+signals+'", dateOp = "'+dateOp+'", trend = "'+trend+'", cons = "'+cons+'", typeStg = "'+typSratg+'", nivel = "'+nivel+'", accType = "'+typeAcc+'" WHERE idfk = '+str(idUser)+' and cod = "'+cod+'"')
			MyDb.commit()
			return True, 'OK'
		except Exception as a:
			pass
			return False, str(a)
	def auth(token, idd):
		try:
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.garratradingacc where tokenTelegram = '"+token+"' and chatId = '"+str(idd)+"' and active is not null")
			account = myCursor.fetchone()
			if account == None:
				return False, None, None,None, 'E001 - Token invalido'
			else: 
				key = bytes(account[6], 'utf-8')
				f = Fernet(key)
				passwd =  f.decrypt(bytes(account[5], 'utf-8'))
				passwd = str(passwd)
				passwd = str(passwd[2:-1])
				return True, account[1], passwd,account[0],'ok'
		except Exception as a:
			return False, None, None,None, str(a)
			pass
	def selUsers():
		try:
			MyDb = connection.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT chatId FROM copytraderone.garratradingacc where active is not null ")
			account = myCursor.fetchall()
			MyDb.close()
			if account == None:
				return False, None
			else: 
				return True, account
		except Exception as a:
			MyDb.close()
			return False, None
class connection:
	def connection():
		MyDb = mysql.connector.connect(
		host="ost",
		user="copone",
		password="#T",
		database="copyone"
		)
		return MyDb
	def connection2():
		MyDb2 = mysql.connector.connect(
		host="44",
		user="alli",
		password="J",
		database="coerone"
		)
		return MyDb2
