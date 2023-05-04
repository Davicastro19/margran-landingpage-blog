from iqoptionapi.stable_api import IQ_Option
import time
import sys
import numpy as np

# Definir parâmetros do backtest
symbol = "EURUSD-OTC"
timeframe = 1
initial_balance = 1000
investment_amount = 100
start_timestamp = 1677651165 # 12 de fevereiro de 2021
end_timestamp = 1677996765 # 19 de fevereiro de 2021

rsi_period = 14 # Período do RSI
rsi_upper_threshold = 70 # Limite superior do RSI para posição de venda
rsi_lower_threshold = 30 # Limite inferior do RSI para posição de compra

# Conectar à API
API = IQ_Option("contatodavisp@outlook.com", "j3112davi")
API.connect()
if not API.check_connect():
    print('Erro ao se conectar')
    sys.exit()
API.change_balance('PRACTICE')  # Utilize a conta demo

# Obter o histórico de velas e calcular o RSI
candles = API.get_candles(symbol, timeframe, start_timestamp, end_timestamp)
prices = np.array([candle['close'] for candle in candles])
rsi = 100 - (100 / (1 + np.divide(np.mean(np.maximum(np.diff(prices), 0)), np.mean(np.maximum(-np.diff(prices), 0)))))[rsi_period-1:]

# Configurar variáveis para o backtest
balance = initial_balance
wins = 0
losses = 0

# Percorrer todas as velas e verificar se uma posição teria sido vencedora ou perdedora
for i in range(rsi_period, len(candles)):
    open_price = candles[i-1]["close"]
    close_price = candles[i]["close"]
    
    # Verificar as regras de entrada e saída baseadas no RSI
    if rsi[i-rsi_period] > rsi_upper_threshold:
        # RSI acima do limite superior indica uma posição de venda
        balance -= investment_amount
        losses += 1
    elif rsi[i-rsi_period] < rsi_lower_threshold:
        # RSI abaixo do limite inferior indica uma posição de compra
        balance += investment_amount * (close_price - open_price)
        wins += 1

# Imprimir os resultados do backtest
print("Saldo final: $", balance)
print("Quantidade de vitórias:", wins)
print("Quantidade de derrotas:", losses)
