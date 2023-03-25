from Controller.message import controlMessage

class file:
    def alterParameter(id,parameter,value):
        try:
            datas = file.get(id)
            if datas:
                datas[parameter] = value
                full = ''
                for data in datas:
                    full += str(datas[data])+','
                full = full[:-1]
                with open(id+'.txt', 'w') as configfile:
                    configfile.write(full)
        except  Exception as a:
            controlMessage.send_msg("class file def alterParameter "+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
            pass
    def create(id):
        try:
            file = open(id+'.txt', 'a')
            file.write('email,pass,1,2.2,0,OFF,ON,4,10,20,ALLWINSIGNALS,OTC,24/12/2021,True,False,key,True,PRATICA,1,2,R$,1,20064,Gale,0,5,OFF')
            file.close()
        except  Exception as a:
            controlMessage.send_msg("class file def create "+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
            pass
    def restoreData(id, data):
        try:
            fileSettings = open(id+'.txt', 'a')
            fileSettings.write(data)
            fileSettings.close()
        except  Exception as a:
            controlMessage.send_msg("class file def restoreData "+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
            pass
    def getDif(id):
        try:
            with open(id+".txt","r+", encoding="UTF-8") as archive:
                nlistt = archive.read()
                archive.close
            return True, nlistt
        except Exception as a:
            return False, a
    def get(id):
        try:
            file = open(str(id)+'.txt', 'r')
            data = file.read()
            data = data.split(',')
            file.close()
        except  Exception as a:
            if 'No such file or directory' in str(a):
                pass
            else:
                controlMessage.send_msg("class file def get "+str(a),'971655878','1856618899:AAGHq3wJkjNqtO5NiasW8jkaKJg6GOcubw0')
            return False
                
        return {
        'email': data[0],
        'passwd': data[1],
        'gale': data[2],
        'factorGale': data[3],
        'nivel': data[4],
        'preStop': data[5],
        'doji': data[6],
        'invest': data[7],
        'stopWin': data[8],
        'stopLoss': data[9],
        'typeSignals': data[10],
        'signals': data[11],
        'date': data[12],
        'finish': data[13],
        'start': data[14],
        'key': data[15],
        'valid': data[16],
        'typeAcc': data[17],
        'touros': data[18],
        'maxSim': data[19],
        'typeEnter': data[20],
        'pay': data[21],
        'PID': data[22],
        'typeStrategy': data[23],
        'factorCiclos': data[24],
        'delay': data[25],
        'trend': data[26]}