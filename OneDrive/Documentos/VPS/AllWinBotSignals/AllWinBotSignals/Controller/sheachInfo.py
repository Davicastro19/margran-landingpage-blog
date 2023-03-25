import json, requests,time
from datetime import datetime
from dateutil import tz

class geral:
    def news(paridade,filtro):
        response = requests.get("http://botpro.com.br/calendario-economico/")
        texto = response.content
        objeto = json.loads(texto)
        if response.status_code == 200 or objeto['success'] == True:
            # Pega a data atual
            data = datetime.now()
            tm = tz.gettz('America/Sao Paulo')
            data_atual = data.astimezone(tm)
            data_atual = data_atual.strftime('%Y-%m-%d')
            tempoAtual = data.astimezone(tm)
            minutos_lista = tempoAtual.strftime('%H:%M:%S')
            # Varre todos o result do JSON
            for noticia in objeto['result']:
                paridade1 = paridade[0:3]
                paridade2 = paridade[3:6]
                # Pega a paridade, impacto e separa a data da hora da API
                moeda = noticia['economy']
                impacto = noticia['impact']
                atual = noticia['data']
                data = atual.split(' ')[0]
                hora = atual.split(' ')[1]
                # Verifica se a paridade existe da noticia e se está na data atual
                if moeda == paridade1 or moeda == paridade2 and data == data_atual:
                    formato = '%H:%M:%S'
                    d1 = datetime.strptime(hora, formato)
                    d2 = datetime.strptime(minutos_lista, formato)
                    dif = (d1 - d2).total_seconds()
                    ## Verifica a diferença entre a hora da noticia e a hora da operação
                    minutesDiff = dif / 60
                    ## Verifica se a noticia irá acontencer 30 min antes ou depois da operação
                    if minutesDiff >= -15 and minutesDiff <= 0 or minutesDiff <= 15 and minutesDiff >= 0:
                        if impacto > int(filtro):
                            return impacto, moeda, hora, True
                    else:
                        pass
                else:
                    pass
        return 0, 0, 0, False
    def Tendencia(par,timeframe,dir, API,idd,telegramTk):
        velas = API.get_candles(par, (int(timeframe) * 60), 20, time.time())
        ultimo = round(velas[0]['close'], 4)
        primeiro = round(velas[-1]['close'], 4)
        diferenca = abs( round( ( (ultimo - primeiro) / primeiro ) * 100, 3) )
        tendencia = "call" if ultimo < primeiro and diferenca > 0.01 else "put" if ultimo > primeiro and diferenca > 0.01 else False
        if tendencia == False:
            tendencia = True
        elif tendencia != dir:
            tendencia = False
        elif tendencia == dir:
            tendencia = True
        #threading.Thread(target=controlParameter.visutrend, args=(par,dir,tendencia,idd,telegramTk),daemon=True).start()
        return tendencia