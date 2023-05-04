from Controller.controlConfig import controlParameter
from cryptography.fernet import Fernet
import mysql.connector
class connectDao:
	def selUsers():
		try:
			MyDb = connection.connection2()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT chat_id FROM copytraderone.contasallwinn where activate = 'active' and typebot = 'LAB'")
			account = myCursor.fetchall()
			MyDb.close()
			if account == None:
				return False, None
			else: 
				return True, account
		except Exception as a:
			MyDb.close()
			return False, None
	def insertAcc(email, senha, valor,order_key, name, product_id, date,tokrn, chat_id, date_c, id_acc):
		try:
			MyDb = connection.connection2()
			myCursor = MyDb.cursor()
			myCursor.execute("SELECT * FROM copytraderone.contasallwinn where email='"+email+"' and typebot = 'LAB'")
			account = myCursor.fetchone()
			if account == None:
				myCursor = MyDb.cursor()
				myCursor.execute("insert into copytraderone.contasallwinn (email, password, value, order_key, name, product_id, activate, token, chat_id, date,acc_id,typebot) VALUES ('"+email+"', '"+senha+"', '"+valor+"', '"+order_key+"', '"+name+"', '"+product_id+"', 'active', 'LAB', '"+chat_id+"', '"+date_c+"', '"+id_acc+"','LAB')")
				MyDb.commit()
				MyDb.close()
				return True,''
			else:
				MyDb.close()
				return False,"JÁ CADASTRADO"
		except Exception as a:
			MyDb.close()
			return False,"ERRO: "+str(a)

	def AuthId(userId):
		try:
			MyDb = connection.connection2()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.contasallwinn where chat_id = '"+str(userId)+"' and activate = 'active' and typebot = 'LAB'")
			account = myCursor.fetchone()
			MyDb.close()
			return True
		except Exception as a:
			##print(a)
			MyDb.close()
			return False
	def updateStrategy(pair,time,filtro,syss,pct,sistema):
		try:
			MyDb2 = connection.connection()
			myCursor = MyDb2.cursor()
			myCursor.execute("SELECT * FROM allwinclub_winlab.strategy where par = '"+str(pair)+"' and time = '"+str(time)+"' and gale = '"+str(filtro)+"' and estrategia = '"+str(syss)+"' and pct >= '"+str(pct)+"'")
			account = myCursor.fetchone()
			MyDb2.close()
			if account != None:
				a = account[2].split('\n')
				i = 0
				resul = ''
				for det in a:
					if i == 0:
						det = sistema
					if det == '':
						det = '\n'
					resul += det
					i+=1
				resul = resul.replace("🧮","")
				resul = resul.replace("🧮","")
				resul = resul.replace("🔽","")
				resul = resul.replace("\n\nPróxima Entrada:","")
				resul = resul.replace("Último Quadrante:","Última análise:")
				resul = resul.replace("Consecutivos:","Sucessivos")
				resul = resul.replace("🔮 ","")
				resul = resul.replace("\n\nComo operar? /help","")
				resul = resul.replace("\n\n","\n")
				resul = resul.replace("Hits","Loss")
				resul = resul.replace("Wins","Win")
				resul = resul.replace("em","-")
				resul = resul.replace("de Acertos","de acessertividade")
				 
					
						

				return True, resul
			else: 
				return False,"Porcentagem abaixo de "+str(pct)+"%"
		except Exception as e:
			#print(e)
			return False,str(e)
	def conwoo():
		try:
			MyDb = connection.connection2()
			myCursor = MyDb.cursor()
			myCursor.execute("select * from copytraderone.secret_api")
			account = myCursor.fetchone()
			MyDb.close()
			if account == None:
				return False, None, None
			else: 
				return True, account[1], account[2]
				
		except Exception as a:
			MyDb.close()
			return False, None, None
	def getParesBd():
		try:
			MyDb = connection.connection2()
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
class connection:
	def connection2():
		MyDb = mysql.connector.connect(
		  host="den1.mysql5.gear.host",
		  user="copytraderone",
		  password="#hsE&tYEXkkdListGT",
		  database="copytraderone"
		)
		return MyDb
	def connection():
		MyDb2 = mysql.connector.connect(
		  host="45.13.59.114",
		  user="allwinclub_davi",
		  password="J3112davi!",
		  database="allwinclub_winlab"
		)
		return MyDb2
