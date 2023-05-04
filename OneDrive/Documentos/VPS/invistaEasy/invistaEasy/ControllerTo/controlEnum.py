from enum  import Enum

class MENSAGE_ERRO(Enum):
    ALL = 'ERRO - contate o suporte com o erro: {0}'
    
    VALIDATE_EMAIL = 'Email: Campo vazio, tente novamente' 
    
    VALIDATE_PASS =  'Senha: Campo vazio, tente novamente'
    
    VALIDATE_ALL = 'Email e Senha são campos obrigatórios'

    MSGE001  = 'Campos invalidos, tente novamente ou contate o suporte  com  Erro: {0}'
class MENSAGE(Enum):
    ALL = '''Olá {0}, seja bem-vindo!

/jurosc - Simular juros composto

/gerenciamento -  Calculadora  para simular SorosGale, Ciclos e Gale

/catalogar - Catalogar estratégia e analisar o mercado atual

/notify - Notificar a cada entrada realizada pela estratégia baseado na config(maximo 4)

/poshit - Notifica somente após um hit

/stop - Para de notificar todas ativas(não é possivel parar só uma)

/ativar - ativar conta

'''
    MSG001 = 'Seu bot está em execução'
    
    MSG002 = 'Conectando, Aguarde 10 seg...'
    
    MSG003 = '''
Você não esta cadastrado. Envie o comprovante para @thisisallwinclub\n
    '''

    MSG004 = '''<b>{0}, só precisamos fazer esta etapa uma vez.

Seu código para me autorizar a executar os comando é {1}.</b>'''

    MSG005 =  '''<b>Comandos:

/login (conctar ou alterar conta)

/goallwin (Par iniciar), 

 /stop (Para parar o bot)

 /update (Alterar a config)

 /helplist (Formato)

 /finish (finalizar e desconectar)

/cmd (comandos)
                            </b>'''

    MSG006 =  "Email invalido ou não cadastrado. se acha estranho ou caso de erro contate o suporte"
    
    MSG007 = 'Ok {0}.... pode ser que esteja alguma operação em andamento.\nAguarde os gales possivelmente.'

    MSG008 = '{0}, já parei'

    MSG009 = '<b>{0},  Ordem executada:\nPar{1}   Valor💶 {2}\nM{3}     Dir{4}\n🧪{5}   -   N{6}\nOp.Digital</b>'
    
    MSG010 = '<b>{0},  Ordem executada:\n💹 {1}   💶 {2}\nⓂ️{3}     🔃{4}\n🧪{5}   -   N{6}\nOp.Binária</b>'

    MSG011 = '<b>{0}, Seu setUp para o dia {10}:\nConta: {1}\nGale:{2} \nP-Stop: {3}\nBanca: R${4}\nEntrada: R${5}\nStop Loss: R${6}\nStop Win: R${7}\nFator Gale: {8}\nQnt. Sinais: {9}\n\nÍniciando agora\n</b>'

    MSG012 = '{0},  Ordem executada:\n<b>Par:</b> {1} <b>Valor:</b> {2}\n<b>Time:</b> M{3} <b>Dir:</b> {4} <b>Ciclos:</b> {5} - <b>Gale:</b> {6}\nOP.DIG'
    MSG013 = '{0},  Ordem executada:\n<b>Par:</b> {1} <b>Valor:</b> {2}\n<b>Time:</b> M{3} <b>Dir:</b> {4} <b>Ciclos:</b> {5} - <b>Gale:</b> {6}\nOP.BIN'

    MSG014 = '{0},  Ordem executada:\nPar: {1} Valor: {2}\n M{3}  Dir: {4} Gale: {5}\nOp.Digital'
    MSG015 = '{0},  Ordem executada:\nPar: {1} Valor: {2}\n M{3}  Dir: {4} Gale: {5}\nOp.Binária'

    MSG016 = 'O.Executada&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{0}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;M{2}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{5}<sup>{4}</sup>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{3}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{1}<br>'
    MSG017 = 'O.Executada&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{0}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;M{2}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{5}<sup>{4}</sup>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{3}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{1}<br>'
