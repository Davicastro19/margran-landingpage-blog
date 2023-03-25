from Controller.datesTimes import date
from cryptography.fernet import Fernet
import mysql.connector, os
class connectDao:
	def saveData(conf,msgid):
		#touros,maxSim,typeStrategy,factorCiclos,factorGale,nivel,preStop,quadrante,signals,typeEnter,doji,gale,invest,stopWin,trend,stopLosstimeFrame,date,pay,finish
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			#print("update  copytraderone.garratradingacc set config2  = '"+conf+"' where chatId = '"+msgid+"'")
			myCursor.execute("update  copytraderone.contasallwinn set conf  = '"+conf+"' where chat_id = '"+msgid+"'")
			MyDb.commit()
			if myCursor.rowcount > 0:
				return True,''
			else:
				return False,''
		except Exception as e:
			MyDb.rollback()
			return False,str(e)
	def selectConfigById(userId):
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT conf FROM copytraderone.contasallwinn where chat_id = '"+str(userId)+"' and activate = 'active' and conf is not null  and typebot = 'BOT' ")
			account = myCursor.fetchone()
			if account == None:
				return False, ''
			else: 
				return True, account[0]
		except Exception as a:
			#print(a)
			return False,str(a)
	def selUsers():
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT chat_id FROM copytraderone.contasallwinn where activate = 'active' and typebot = 'BOT'")
			account = myCursor.fetchall()
			if account == None:
				return False, None
			else: 
				return True, account
		except Exception as a:
			return False, None
	
	def signals(listOption):
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			if listOption =='H1':
				myCursor.execute("select * from  copytraderone.sinaiss where id = 1")
			elif listOption =='M30':
				myCursor.execute("select * from  copytraderone.sinaiss where id = 2")
			elif listOption =='M15':	
				myCursor.execute("select * from  copytraderone.sinaiss where id = 3")
			elif listOption =='M5':	
				myCursor.execute("select * from  copytraderone.sinaiss where id = 15")
			elif listOption =='M1':	
				myCursor.execute("select * from  copytraderone.sinaiss where id = 9")
			elif listOption =='Lista':
				myCursor.execute("select * from  copytraderone.sinaiss where id = 4")
			elif listOption =='OTC':	
				myCursor.execute("select * from  copytraderone.sinaiss where id = 5")
			elif listOption =='PrAc':	
				myCursor.execute("select * from  copytraderone.sinaiss where id = 6")
			else:
				myCursor.execute("select * from  copytraderone.sinaiss where id = 2")
			sinais = myCursor.fetchone()
			if sinais != None:
				return sinais[1],sinais[2]
			else: 
				return None,None
		except:
			return None,None
	
	
	def authenticateById(userId):
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.contasallwinn where chat_id = '"+str(userId)+"' and activate = 'active' and typebot = 'BOT'")
			account = myCursor.fetchone()
			if account == None:
				return False
			else: 
				return True
		except Exception as a:
			#print(a)
			return False
	def insertAccount(email, senha, valor,order_key, name, product_id, date, token, chat_id, date_c, id_acc):
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT * FROM copytraderone.contasallwinn where email='"+email+"' and  typebot = 'BOT'")
			account = myCursor.fetchone()
			if account == None:
				myCursor = MyDb.cursor()
				myCursor.execute("insert into copytraderone.contasallwinn (email, password, value, order_key, name, product_id, activate, token, chat_id, date,acc_id,typebot) VALUES ('"+email+"', '"+senha+"', '"+valor+"', '"+order_key+"', '"+name+"', '"+product_id+"', 'active', '"+token+"', '"+chat_id+"', '"+date_c+"', '"+id_acc+"','BOT')");
			else:
				myCursor = MyDb.cursor()
				myCursor.execute("DELETE FROM copytraderone.contasallwinn WHERE id = "+str(account[0]))
				MyDb.commit()
				myCursor = MyDb.cursor()
				myCursor.execute("insert into copytraderone.contasallwinn (email, password, value, order_key, name, product_id, activate, token, chat_id, date,acc_id,typebot) VALUES ('"+email+"', '"+senha+"', '"+valor+"', '"+order_key+"', '"+name+"', '"+product_id+"', 'active', '"+token+"', '"+chat_id+"', '"+date_c+"', '"+id_acc+"','BOT')");
			MyDb.commit()
			myCursor.close()
			MyDb.close()
			return True,''
		except Exception as a:
			#print(a)
			return False, str(a)
	
	def sinaisaw(x):
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			if x == 1:
				myCursor.execute("select * from  copytraderone.sinais where id = 1")
			else:
				myCursor.execute("select * from  copytraderone.sinais where id = 2")
			sinais = myCursor.fetchone()
			if sinais != None:
				MyDb.close()
				myCursor.close()
				return sinais[1],sinais[2]
			else: 
				MyDb.close()
				myCursor.close()
				return None,None
			
		except Exception as a:
			return None,None
	
	def selectStart(idsecret,cod,idfk):
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT * FROM copytraderone.garraaccconfig where cod = '"+cod+"' and idsecret = '"+idsecret+"' and idfk = "+str(idfk)+"")
			config = myCursor.fetchone()
			if config == None:
				return False,None,None,None,None,None,None,None,None,None,None,None,None,None,None, 'Não há configurações cadastradas use /go ou contate o suporte🙄🙄'
			else:
				return True, config[4],config[5],config[6],config[7],config[8],config[9],config[10],config[11],config[12],config[13],config[14],config[15],config[16],config[17],'ok'
		except Exception as a:
			return False, None,None,None,None,None,None,None,None,None,None,None,None,None,None,'contate o suporte com o erro - '+str(a) 


	def selectList(lista):
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.garratradinsinais where type = '"+lista+"'")
			sinais = myCursor.fetchone()
			if sinais == None:
				return False, None, None, None, None, None, 'MSG003 Lista inexistente'
			else: 
				if sinais[3] < str(date.currentDateString()):
					return False, None, None, None, None, None,'MSG004  Lista desatualizada"'
				else:
					return True, sinais[1],sinais[2],sinais[3],sinais[4],sinais[5],'ok'
		except Exception as a:
			return False, None, None, None, None, None, str(a)
			

			
	def conwoo():
		try:
			MyDb = connector.connection()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.secret_api")
			account = myCursor.fetchone()
			if account == None:
				return False, None, None
			else: 
				return True, account[1], account[2]
		except Exception as a:
			return False, None, None
class connector:
	def connection():
		MyDb = mysql.connector.connect(
		  host="den1.mysql5.gear.host",
		  user="copytraderone",
		  password="#hsE&tYEXkkdListGT",
		  database="copytraderone"
		)
		return MyDb
	
