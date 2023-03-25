from enum  import Enum

class MENSAGE_ERRO(Enum):
    ALL = 'ERRO - contate o suporte com o erro: {0}'
    
    VALIDATE_EMAIL = 'Email: Campo vazio, tente novamente' 
    
    VALIDATE_PASS =  'Senha: Campo vazio, tente novamente'
    
    VALIDATE_ALL = 'Email e Senha são campos obrigatórios'

    MSGE001  = 'Campos invalidos, tente novamente ou contate o suporte  com  Erro: {0}'
class MENSAGE(Enum):
    ALL = '''Olá {0}, seja bem-vindo!

1ª faça login: '👤 Login''

2ª configure os parametros: '⚙️ Configuração geral'
3ª iniciar e alterar o tipo de conta '▶️ Iniciar'

utilize '⏸ Parar' para parar e '📴 Sair e Desconectar' finaliza o bot

sobre comandos clique em /cmd

Responda com seus dados de acesso à corretora
e com as configurações que podem ser alterardas a qualquer momento.


OBS: Verifique minúsculo e maiúsculo em cada palavra. Todos os dados são criptografados.'''
    MSG001 = 'Seu bot está em execução'
    
    MSG002 = 'Conectando, Aguarde 4 seg...'
    
    MSG003 = '''
Você não esta cadastrado. Envie o comprovante para @thisisallwinclub\n
    '''

    MSG004 = '''<b>{0}, só precisamos fazer esta etapa uma vez.

Seu código para me autorizar a executar os comando é {1}.</b>'''

    MSG005 =  '''<b>Comandos:

'👤 Login' (conctar ou alterar conta)

'▶️ Iniciar' (Par iniciar)

'⏸ Parar' (Para parar o bot)

'🛠 Configurações especificas' (Alterar individualmente uma configução)

'⚙️ Configuração geral' (Alterar a config)

/helplist (Formato)

'📴 Sair e Desconectar' (finalizar e desconectar)

/cmd (comandos)

'📚 Informação' (Sua configurações em detalhes)
                            </b>'''

    MSG006 =  "Email invalido ou não cadastrado. se acha estranho ou caso de erro contate o suporte"
    
    MSG007 = 'Ok {0}.... pode ser que esteja alguma operação em andamento.\nAguarde os gales possivelmente.'

    MSG008 = '{0}, '

    MSG009 = '<b>{0},  Ordem executada:\n💹: {1}\n💶: {2}\nⓂ️: M{3}\n🔃: {4}\n🧪 {5}º - E{6}º\nOp.Digital</b>'
    MSG010 = '<b>{0},  Ordem executada:\n💹: {1}\n💶: {2}\nⓂ️: M{3}\n🔃: {4}\n🧪 {5}º - E{6}º\nOp.Binária</b>'

    MSG011 = '<b>{0}, Seu setUp para o dia {10}:\nConta: {1}\nGALE:{2} \nP-Stop: {3}\nBanca: R${4}\nEntrada: R${5}\nStop Loss: R${6}\nStop Win: R${7}\nFator GALE: {8}\nQnt. Sinais: {9}\n\nÍniciando agora\n</b>'

    MSG012 = '<b>{0}, Ordem executada:\n💹: {1}\n💶: {2}\nⓂ️: M{3}\n🔃: {4} 🆑 {5} - G{6}\nOP.DIG</b>'
    MSG013 = '<b>{0}, Ordem executada:\n💹: {1}\n💶: {2}\nⓂ️: M{3}\n🔃: {4} 🆑 {5} - G{6}\nOP.BIN</b>'

    MSG014 = '<b>{0},  Ordem executada:\n💹: {1}\n💶: {2}\nⓂ️: M{3}\n🔃: {4} G{5}\nOp.Digital</b>'
    MSG015 = '<b>{0},  Ordem executada:\n💹: {1}\n💶: {2}\nⓂ️: M{3}\n🔃: {4} G{5}\nOp.Binária</b>'

    MSG016 = 'O.Executada&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{0}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;M{2}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{5}<sup>{4}</sup>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{3}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{1}<br>'
    MSG017 = 'O.Executada&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{0}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;M{2}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{5}<sup>{4}</sup>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{3}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{1}<br>'
