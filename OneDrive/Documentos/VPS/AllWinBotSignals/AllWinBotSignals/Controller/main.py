from Controller.fileSettings import file
from Controller.controlEnum import MENSAGE
from iqoptionapi.stable_api import IQ_Option
from Controller.controlDao import connectDao
from Controller.datesTimes import hour,date,dateHours
from Controller.message import controlMessage
from Controller.controlConfig import controlValue, controlOptions
from time import sleep
from cryptography.fernet import Fernet
from Controller.sheachInfo import geral
from datetime import datetime
from dateutil import tz
import time,json, requests, sys,os, threading

class comand:
    def invest(API,name,Sgale,balance,idd,gale,investPct,Par,Valor,base,dir,timeFrame, ciclo,posDoji,telegramTk,Options,checkSorosGale,Wins, loss, ns, nivel,r,NV,FG,CL,preStop,stopLoss,stopWin, Pay):
        try:
        #if True:
            investedValue = base
            if ns > 0:
                investedValue = Valor
            if Options == "BD":
                lucro = Valor 
                gale = 0
                Time = int(timeFrame[1:])
                b = 'ok'
                while gale <= Sgale:
                    if preStop == "ON":
                        stop = controlValue.StopLo(API, stopLoss,stopWin, idd, balance,telegramTk)
                        stopw = controlValue.StopWi(API, stopLoss,stopWin, idd, balance,telegramTk)
                    else:
                        stop = False
                        stopw = False
                    if stop == False and stopw == False:
                        if checkSorosGale== "ON":
                            if gale > 0:
                                investedValue,r,ns,nivel = controlValue.calc(base,r,ns,nivel,NV)
                        else:
                            if gale > 0: 
                                investedValue = investedValue * FG
                        statusBi = True
                        investedValue = round(float(investedValue),2)
                        if  Pay == 0: 
                            #print(investedValue)
                            statusBi,idBi,expred,now = API.buy(investedValue,Par, dir, Time)
                            if statusBi == False and 'O tempo para comprar essa opção já terminou' not in str(idBi):
                                statusBi,idBi = API.check_win_v46(expred,now,investedValue,Par, dir, Time)
                            if statusBi:
                                msg4 = ''
                                if checkSorosGale == "ON":
                                    msg4 = MENSAGE.MSG016.value.format(Par,investedValue,Time,dir.upper(),gale,str(investPct)[:-3])
                                    controlMessage.send_msg(MENSAGE.MSG010.value.format(name,Par,investedValue,Time,dir.upper(),ns,nivel),idd, telegramTk)
                                elif CL == "ON":
                                    msg4 = MENSAGE.MSG016.value.format(Par,investedValue,Time,dir.upper(),gale,str(investPct)[:-3])
                                    controlMessage.send_msg(MENSAGE.MSG013.value.format(name,Par,investedValue,Time,dir.upper(),ciclo,gale),idd, telegramTk)	
                                else:
                                    controlMessage.send_msg(MENSAGE.MSG015.value.format(name,Par,investedValue,Time,dir.upper(),ns,nivel),idd, telegramTk)
                                while statusBi:
                                    lucro,investPctf = API.check_win_v3(idBi)
                                    if lucro > 0:
                                        Wins+=1
                                        if nivel >= 2:
                                            nivel = 1
                                            ns =0
                                        elif nivel == 1:
                                            nivel += 1
                                        if loss < 0:
                                            ns= 2
                                        statusBi = False
                                        if gale < 1:
                                            types = "biw"
                                        else:
                                            types = "biwg"
                                        threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, lucro, investedValue,Time, types,balance, idd, investPct,gale,investPctf,'',telegramTk,dir, idBi,msg4),daemon=True).start()
                                        gale = 100
                                    elif lucro < 0 :
                                        loss+=1
                                        ns += 1
                                        nivel += 1
                                        if nivel >= 2:
                                            nivel = 1
                                        statusBi = False
                                        if gale < 1:
                                            types = "bil"
                                        else:
                                            types ="bilg" 
                                        threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, lucro, investedValue,Time, types ,balance, idd, investPct,gale,investPctf,'',telegramTk,dir,idBi,msg4),daemon=True).start()
                                        gale += 1							
                                    else:
                                        loss+=1
                                        ns += 1
                                        nivel += 1
                                        if nivel >= 2:
                                            nivel = 1
                                        if gale < 1:
                                            types = "bie"
                                        else:
                                            types ="bieg"
                                        statusBi = False
                                        threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, lucro, investedValue,Time, types,balance, idd, investPct,gale,investPctf,'',telegramTk,dir, idBi,msg4),daemon=True).start()
                                        gale += 1
                                        if posDoji == "OFF":
                                            gale=100
                            else:
                                msg4 = ''
                                threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, 0, investedValue,Time, "fob",balance, idd, investPct,gale,"","",telegramTk,dir, idBi,msg4),daemon=True).start()			
                                gale = 100
                                b = "block"
                        else:
                            if  Pay == 0:
                                msg4 = ''
                                threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, 0, investedValue,Time, "fob",balance, idd, investPct,gale,"","",telegramTk,dir, 'Payout',msg4),daemon=True).start()			
                                statusDi = False
                                gale = 100
                                b = "block"
                        if Pay != 0:
                            #print(investedValue)
                            statusDi,idDi = API.buy_digital_spot_v2(Par, investedValue, dir, Time)
                            if statusDi:
                                msg4 = ''
                                if checkSorosGale == "ON":
                                    msg4 = MENSAGE.MSG017.value.format(Par,investedValue,Time,dir.upper(),gale,str(investPct)[:-3])
                                    controlMessage.send_msg(MENSAGE.MSG009.value.format(name,Par,investedValue,Time,dir.upper(),ns,nivel),idd, telegramTk)
                                elif CL == "ON":
                                    msg4 = MENSAGE.MSG017.value.format(Par,investedValue,Time,dir.upper(),gale,str(investPct)[:-3])
                                    controlMessage.send_msg(MENSAGE.MSG012.value.format(name,Par,investedValue,Time,dir.upper(),ciclo,gale),idd, telegramTk)
                                else:
                                    controlMessage.send_msg(MENSAGE.MSG014.value.format(name,Par,investedValue,Time,dir.upper(),ns,nivel),idd, telegramTk)
                                
                                while statusDi:
                                    statusto,lucro,investPctf = API.check_win_digital_v2(idDi)
                                    if statusto:
                                        if lucro > 0:
                                            Wins+=1
                                            if nivel >= 2:
                                                nivel = 1
                                                ns =0
                                            elif nivel == 1:
                                                nivel += 1
                                            if loss < 0:
                                                ns= 2
                                            statusDi = False
                                            if gale < 1:
                                                types = "diw"
                                            else:
                                                types = "diwg"
                                            threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, lucro, investedValue,Time, types,balance, idd, investPct,gale,str(investPctf)[:10],"",telegramTk,dir, idDi,msg4),daemon=True).start()
                                            gale = 100
                                        elif lucro < 0 :
                                            loss+=1
                                            ns += 1
                                            nivel += 1
                                            if nivel >= 2:
                                                nivel = 1
                                            statusDi = False
                                            if gale < 1:
                                                types = "dil"
                                            else:
                                                types ="dilg" 
                                            threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, lucro, investedValue,Time, types ,balance, idd, investPct,gale,str(investPctf)[:10],"",telegramTk,dir, idDi,msg4),daemon=True).start()
                                            gale += 1							
                                        else:
                                            loss+=1
                                            ns += 1
                                            nivel += 1
                                            if nivel >= 2:
                                                nivel = 1
                                            statusDi = False
                                            if gale < 1:
                                                types = "die"
                                            else:
                                                types ="dieg"
                                            statusDi = False
                                            threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, lucro, investedValue,Time, types,balance, idd, investPct,gale,str(investPctf)[:10],"",telegramTk,dir, idDi,msg4),daemon=True).start()
                                            gale += 1
                                            if posDoji == "OFF":
                                                gale=100
                            else:
                                msg4 = ''
                                threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, 0, investedValue,Time, "fod",balance, idd, investPct,gale,"","",telegramTk,dir, idDi,msg4),daemon=True).start()			
                                gale = 100
                                b = "block"
                        else:
                            
                            if Pay != 0:
                                msg4 = ''
                                threading.Thread(target=controlMessage.sendWinOrLossOrDoji, args=(API,name, Par, 0, investedValue,Time, "fod",balance, idd, investPct,gale,"","",telegramTk,dir, 'Payout',msg4),daemon=True).start()			
                                gale = 100
                                b = "block"
                                
                    else:
                        gale = 100
                if lucro == 0 or lucro == 0.0:
                    lucro = Valor
                ##print('saiu')
                return lucro, b, Wins, loss, ns, nivel
        except Exception as a:
            #print(a)
            controlMessage.send_msg(str(a),idd, telegramTk)
            return Valor, "ok",0, 0, 0, 0
    def start(chatId,telegramTk):
        try:
        #if True:
            file.alterParameter(str(chatId),'finish',False)
            parameters  = file.get(chatId)
            message ='Start: '+'Iniciado\nConta: '+ 'Conectado\nID:'+str(parameters['PID']) if parameters['start']=="True" else 'Desconectado \nID:'+str(parameters['PID'])   if parameters['start']=="True" else 'Parado'+'\nConta: '+ 'Conectado. \nID:'+str(parameters['PID']) if parameters['start']=="True" else 'Desconectado \nID:'+str(parameters['PID'])  
            controlMessage.send_msg(message, chatId,telegramTk)
            key = bytes(parameters['key'], 'utf-8')
            f = Fernet(key)
            passwd =  f.decrypt(bytes(parameters['passwd'], 'utf-8'))
            passwd = str(passwd)
            passwd = str(passwd[2:-1])
            API = IQ_Option(parameters['email'], passwd)
            API.connect()
            parameters  = file.get(chatId)
            while parameters['start'] == 'True':
                parameters  = file.get(chatId)
                if API.check_connect():
                    if 'PRA' in parameters['typeAcc']:
                        typeAccount = 'PRACTICE'
                    else:
                        typeAccount = 'REAL'
                    dateList =parameters['date']
                    listOption = ''
                    userlistSignalsos = API.get_profile_ansyc()
                    name = userlistSignalsos["name"]  
                    API.change_balance(typeAccount)
                    balance = API.get_balance()
                    if parameters['typeEnter'] == '%':
                        stopLoss = float((balance * float(parameters['stopLoss'])) / 100)
                        stopWin = float((balance * float(parameters['stopWin'])) / 100)
                        stopWin = balance + stopWin
                        stopLoss = balance - stopLoss
                        stopWin = round(float(stopWin),2)  
                        stopLoss = round(float(stopLoss),2)
                        investment = float(parameters['invest']) * float(balance)
                        investment = round(float(investment / 100),2)
                        if investment < 2:
                            investment = 2
                        if parameters['typeStrategy'] == "SorosGale":
                            if investment < 4:
                                investment = 4
                    else:
                        stopLoss = float((balance - float(parameters['stopLoss'])))
                        stopWin = float((balance + float(parameters['stopWin'])))
                        stopWin = round(float(stopWin),2)  
                        stopLoss = round(float(stopLoss),2)
                        investment = round(float(parameters['invest']),2)
                    ok = False
                    if parameters['typeSignals'] == "Meus Sinais":
                        listOption = 'MEUS SINAIS'
                        ok = True
                        dateList = parameters['date']
                        listOn  = parameters['signals'].split("\n")
                        controlMessage.send_msg('Carregando  {0}'.format(listOption), chatId,telegramTk)
                        while dateList != str(date.currentDateString()) and parameters['start'] == "True":
                            time.sleep(10)
                            parameters  = file.get(chatId)
                            dateList = parameters['date']
                            pass
                    else:
                        ok = True
                        if parameters['signals'] =='M15-24h':										  
                            listOption = 'M15'
                        elif parameters['signals'] =='M30-24h':										  
                            listOption = 'M30'
                        elif parameters['signals'] =='H1-24h':										  
                            listOption = 'H1'
                        elif parameters['signals'] =='M5-24h':										  
                            listOption = 'M5'
                        elif parameters['signals'] =='LISTA':										  
                            listOption = 'Lista'
                        elif parameters['signals'] =='OTC':										  
                            listOption = 'OTC'
                        elif parameters['signals'] =='PRICE':									  
                            listOption = 'PrAc'
                        else:
                            listOption = 'Lista'
                        controlMessage.send_msg('Carregando meus armamentos de {0}...'.format(listOption),chatId,telegramTk)
                        listSignals,dateListTo = connectDao.signals(listOption)
                        if listSignals != None:
                            listOn = listSignals.split("\n")
                        else:
                            dateListTo = "31/01/2000"
                            listOn = ['']
                        while (dateListTo != dateList) and parameters['start'] == "True":
                            listSignals,dateListTo = connectDao.signals(listOption)
                            if listSignals != None:
                                listOn = listSignals.split("\n")
                            else:
                                listOn = ['']
                            time.sleep(10)
                            parameters  = file.get(chatId)
                            dateList =parameters['date']
                    if ok:
                        Wins = 0
                        loss = 0
                        msgExit = 'n'
                        nivel = 0
                        r = 'n'
                        ctt = 0
                        ns  = 0
                        ciclo = 0
                        gale = 0
                        lucro = 0
                        ok = 'ok'
                        blocklist = []
                        s = 0
                        pars = ''
                        tm = ''
                        delay = int(parameters['delay'])
                        if listOn != []:
                            text=''+str(name)+', SEU SET :\n👤: '+str(parameters['typeAcc'])+'\n〽️: '+str(parameters['typeStrategy'])+'\n💰: R$'+str(balance)+'\n💶: R$'+str(investment)+'\n🥵: R$'+str(stopLoss)+'\n🤑: R$'+str(stopWin)+'\n\nEstou preparado! Vamos! - '+str(listOption)+'\n\n+Detalhes: 📑'
                            controlMessage.send_msg(text, chatId, telegramTk)
                            while parameters['start'] == 'True':
                                try:
                                #if True:
                                    msgExit = 'n'
                                    if hour.currentSecondsString() >= '51' and  hour.currentSecondsString() <= '53' and listOption == "PrAc" :
                                        listSignals,dateList = connectDao.signals(listOption)
                                        if listSignals != None:
                                            listOn = listSignals.split("\n")	
                                        if listOn != [] and listOn != ['']:
                                            while True:
                                                if listOn != [] and listOn != ['']:
                                                    details = listOn[0].split(';')
                                                    if dateHours.dateTimeNowForString() > dateHours.intervalSeconds(""+dateList+" "+details[2]+""):
                                                        listOn.remove(listOn[0])
                                                    else:
                                                        break
                                                else:
                                                    break
                                    elif hour.currentSecondsString() >= '45' and  hour.currentSecondsString() <= '47' and parameters['typeSignals'] != "Meus Sinais" :
                                            listSignals,dateList = connectDao.signals(listOption)
                                            if listSignals != None:
                                                listOn = listSignals.split("\n")
                                            else:
                                                dateList = date.currentDateString()
                                            if listOn != [] and listOn != ['']:
                                                while True:
                                                    if listOn != [] and listOn != ['']:
                                                        details = listOn[0].split(';')
                                                        if dateHours.dateTimeNowForString() > dateHours.intervalSeconds(""+dateList+" "+details[2]+""):
                                                            listOn.remove(listOn[0])
                                                        else:
                                                            break
                                                    else:
                                                        break
                                    elif hour.currentSecondsString() >= '45' and  hour.currentSecondsString() <= '47' and parameters['typeSignals'] == "Meus Sinais":
                                            listOn  = parameters['signals'].split("\n")
                                            dateList = parameters['date']
                                            if listOn != [] and listOn != ['']:
                                                while True:
                                                    if listOn != [] and listOn != ['']:
                                                        details = listOn[0].split(';')
                                                        if dateHours.dateTimeNowForString() > dateHours.intervalSeconds(""+dateList+" "+details[2]+""):
                                                            listOn.remove(listOn[0])
                                                        else:		
                                                            break
                                                    else:
                                                        break	
                                    
                                    if listOn != [] and listOn != ['']:
                                        details = listOn[0].split(';')
                                        plo = dateHours.timestamp_converter()
                                        pp = details[2]
                                        fsi = '%H:%M:%S'
                                        dif = abs((datetime.strptime(plo, fsi) - datetime.strptime(pp, fsi)).total_seconds())
                                        #print(dif)
                                        if float(dif)< -3.0 or (pars == details[1] and tm == details[2]):
                                            listOn.remove(listOn[0])
                                            #print("remove "+str(listOn[0]))
                                        else:
                                            if parameters['touros'] != '0':
                                                if  dif >= float(40) and dif <= float(41):
                                                    blocklist = []
                                                    impacto, moeda, hora, stts = geral.news(details[1],parameters['touros'])
                                                    if stts:
                                                        blocklist.append(details[1])
                                                        blocklist.append(impacto)
                                                        blocklist.append(hora)
                                                        blocklist.append(moeda)
                                            if tm != details[2]:
                                                ctt = 1
                                            else:
                                                ctt += 1
                                            valid = True
                                            #print(float(dif),' <= ',8.0+float(delay))
                                            if float(dif) <= 1.0+float(delay) and float(dif) >= -4.0 and ctt <= int(parameters['maxSim']) and (pars != details[1] or tm != details[2]):
                                                if parameters['touros'] != '0':
                                                    if blocklist != []:
                                                        if blocklist[0] == details[1]:
                                                            text = "📊"+str(listOn[0])+"\n\n⚠️ A ORDEM FOI BLOQUEADA\n"+' NOTÍCIA COM IMPACTO DE '+str(blocklist[1]) +' TOUROS NA MOEDA '+str(blocklist[3]) +' ÀS '+str(blocklist[2])+'!'
                                                            controlMessage.send_msg(text, chatId, telegramTk)
                                                            valid = False
                                                            listOn.remove(listOn[0])
                                                if parameters['trend'] == 'ON' and valid == True:
                                                    if geral.Tendencia(details[1],str(details[0])[1:],str(details[3]).lower(), API,chatId,telegramTk) == False:
                                                        text = "📊"+str(listOn[0])+"\n\n⚠️ A ORDEM FOI BLOQUEADA\n"+' DIREÇÃO CONTRARIA A TENDÊNCIA!'
                                                        controlMessage.send_msg(text, chatId, telegramTk)
                                                        valid = False
                                                        listOn.remove(listOn[0])
                                                if valid:
                                                    API.connect()
                                                    API.change_balance(typeAccount)
                                                    listOn.remove(listOn[0])
                                                    pars = details[1]
                                                    if ok == "ok":
                                                        base = investment
                                                        base =  round(float(base),2)
                                                        Valor = base
                                                    if parameters['typeStrategy'] == "Fixa" or parameters['typeStrategy'] == "Gale":
                                                        ciclo = 0
                                                        t = threading.Thread(target=comand.invest, args=(API,name,int(parameters['gale']),balance,chatId,gale,details[2],str(details[1]),round(float(Valor),2),round(float(base),2),str(details[3]).lower(),str(details[0]),ciclo,parameters['doji'],telegramTk,"BD","ON" if parameters['typeStrategy'] == "SorosGale" else "OFF",Wins, loss, ns, nivel,r,int(parameters['nivel']),float(parameters['factorGale']),"ON" if parameters['typeStrategy'] == "Ciclos" else "OFF",parameters['preStop'],stopLoss,stopWin,int(parameters['pay'])),daemon=True)
                                                        t.start()	
                                                        s = 1
                                                        if parameters['signals'] !='PRICE':
                                                            if listOn == []:
                                                                while t.is_alive():
                                                                    pass
                                                    else:
                                                        if parameters['typeStrategy'] == "SorosGale" :
                                                            Valor,r,ns,nivel = controlValue.calc(base,r,ns,nivel,int(parameters['nivel']))
                                                            ciclo = 0
                                                        if ciclo < int(parameters['nivel'])+1 and ciclo > 0:
                                                            Valor = round(float(abs(lucro)), 2) * float(parameters['factorCiclos'])
                                                        lucro, ok, Wins, loss, ns, nivel = comand.invest(API,name,int(parameters['gale']),balance,chatId,gale,details[2],str(details[1]),round(float(Valor),2),round(float(base),2),str(details[3]).lower(),str(details[0]),ciclo,parameters['doji'],telegramTk,"BD","ON" if parameters['typeStrategy'] == "SorosGale" else "OFF",Wins, loss, ns, nivel,r,int(parameters['nivel']),float(parameters['factorGale']),"ON" if parameters['typeStrategy'] == "Ciclos" else "OFF",parameters['preStop'],stopLoss,stopWin,int(parameters['pay']))
                                                        if ok == "ok":
                                                            if parameters['typeStrategy'] == "Ciclos":
                                                                if lucro <= 0:  
                                                                    ciclo += 1
                                                                else:
                                                                    ciclo = 0
                                                        else:
                                                            if parameters['typeStrategy'] == "SorosGale":
                                                                ciclo = 0
                                                                Valor = lucro
                                                            if parameters['typeStrategy'] == "Ciclos":	
                                                                lucro = round(lucro / float(parameters['factorCiclos']),2)
                                                    if tm == details[2]:
                                                        ctt += 1 
                                                    else:
                                                        ctt = 1
                                                    tm = details[2]	
                                    Stops, rs = controlValue.StopLoWi(API, stopLoss,stopWin, chatId, balance,telegramTk)
                                    if Stops:
                                        if s == 1 and rs == 'L' or s == 1 and rs == 'W':
                                            while t.is_alive():
                                                pass
                                            Stop = controlValue.Stopvery(API, stopLoss,stopWin, chatId, balance,telegramTk)
                                            if Stop :
                                                file.alterParameter(str(chatId),'start','False')
                                                parameters = file.get(chatId)
                                                controlMessage.AttSis(API, stopWin, stopLoss,telegramTk, balance,name,chatId,listOption)
                                                msgExit = 's'
                                                listOn = []
                                                break
                                        elif s != 1 and rs == 'W' or  s != 1 and rs == 'L':
                                            Stop = controlValue.Stopvery(API, stopLoss,stopWin, chatId, balance,telegramTk)
                                            if Stop :
                                                file.alterParameter(str(chatId),'start','False')
                                                parameters = file.get(chatId)
                                                controlMessage.AttSis(API, stopWin, stopLoss,telegramTk, balance,name,chatId,listOption)
                                                msgExit = 's'
                                                listOn = []
                                                break
                                    parameters = file.get(chatId)
                                except Exception as a:
                                    if "Connection is already close" in str(a) or "Foi forçado o cancelamento de uma conexão existente pelo host remoto" in str(a) or  "Websocket connection close" in str(a):
                                        parameters = file.get(chatId)
                                        key = bytes(parameters['key'], 'utf-8')
                                        f = Fernet(key)
                                        passwd =  f.decrypt(bytes(parameters['passwd'], 'utf-8'))
                                        passwd = str(passwd)
                                        passwd = str(passwd[2:-1])
                                        #API = validate.verify(API,parameters['email'], passwd,typeAccount)
                                        Check = API.check_connect()
                                        if Check == True:
                                            API.change_balance(typeAccount)
                                            controlMessage.send_msg('Conectado Novamente', chatId, telegramTk)
                                        else:
                                            controlMessage.send_msg('Não foi possivel se conectar, Reinicie', chatId, telegramTk)
                                    else:
                                        controlMessage.send_msg("WINTEL 1"+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
                                        controlMessage.send_msg("você foi desconectado.",chatId,telegramTk)
                                        file.alterParameter(str(chatId),'start','False')
                                        parameters = file.get(chatId)
                                        break
                            if msgExit != 's':
                                controlMessage.send_msg(listOption+' - Finalizado', chatId, telegramTk)
                                controlMessage.AttSis(API, stopWin, stopLoss,telegramTk, balance,name,chatId,listOption)		
                        else:
                            controlMessage.send_msg(listOption+' - Finalizado', chatId, telegramTk)
                else:
                    controlMessage.send_msg("você foi desconectado ",chatId,telegramTk)
                    file.alterParameter(str(chatId),'start','False')
                file.alterParameter(str(chatId),'start','False')
        except Exception as a:
            controlMessage.send_msg("WINTEL 2"+str(a), '971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
            if "Connection is already close" in str(a) or "Foi forçado o cancelamento de uma conexão existente pelo host remoto" in str(a) or  "Websocket connection close" in str(a):
                text='<b>••••••••••••••AVISO•••••••••••\n&#x1f916;: Não Foi possivel conectar com a IQ WebS Erro servidor, Tente novamente em 1 min. ou contate o suporte!☞\n••••••••••••••••••••••••••••••••••</b>' 
                controlMessage.send_msg(text, chatId,telegramTk)
                pass
            else:
                text='<b>••••••••••••••AVISO•••••••••••\n&#x1f916;: Não Foi possivel conectar Erro desconhecido: '+str(a)+'\n••••••••••••••••••••••••••••••••••</b>'
                controlMessage.send_msg(text, chatId,telegramTk)
            controlMessage.send_msg("você foi desconectado.",chatId,telegramTk)