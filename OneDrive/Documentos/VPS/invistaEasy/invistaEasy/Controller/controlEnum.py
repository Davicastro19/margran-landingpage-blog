from enum  import Enum

class MENSAGE_ERRO(Enum):
    ALL = 'ERRO - contate o suporte com o erro: {0}'
    
    VALIDATE_EMAIL = 'Email: Campo vazio, tente novamente' 
    
    VALIDATE_PASS =  'Senha: Campo vazio, tente novamente'
    
    VALIDATE_ALL = 'Email e Senha são campos obrigatórios'

    MSGE001  = 'Campos invalidos, tente novamente ou contate o suporte  😤😒🙄 com  Erro: {0}'
class MENSAGE(Enum):
    ALL = '''
    🤖:Torne-se um membro😚\nclique em /start
\n
Já aviso te antemão que esse valor esta barato de mais e que esta previsto um aumento, aproveita a oportunidade\n
\n
Entre em contato com @SrDevTrader\n
\n
    '''
    MSG001 = '🤖:Seu bot ja está em execução ta com amnésia❓ 🤨🤔,  Maasss em caso de erro contate o suporte😤😒🙄🙄🙄'
    
    MSG002 = '🤖:Conectando, Aguarde em média 5seg...'
    
    MSG003 = '''
https://www.neoncatalogador.online/

AJUDE A MANTER AS FERRAMENTAS DE FORMA GRATUITA.
E A FAZERMOS MELHORIAS
DOAÇÕES: PIX - EMAIL: davi18827@gmail.com (C6 Bank)

Solicite uma melhoria ou algo que pode ser util para você.
https://t.me/ProgamadorReact

🤖: Bem Vindo ao INVISTA EASY.
OS COMANDOS SÃO:

📊TENDÊNCIA📊 (Analisar a tendência do mercado força compradora ou vendedora)

📝CHECK LIST📝(Fazer checkin de win, loss e doji de qualquer hora e dia existente)

CATALOGAÇÕES CRIPTO E MERCADO NÃO OTC SERVE PARA QUALQUER CORRETORA:
💹CATALOGAR ESTRATÉGIA💹(Catalogar a assertividade de padrões: 14 Estratégias. M1, M5, e M15. Até G5. de 12 até 192 Quadrantes)

📡NOTÍCIAS📡(Saber as notiícias do mercado para uma melhor assertividade nas operações)

🔰CATALOGAR SINAIS🔰(Faça sua Propria lista de sinais para usar ou sua sala de sinais)

🔰CATALOGAR SINAIS II🔰(Faça sua Propria lista de sinais para usar ou sua sala de sinais)

🔢CALCULADORAS🔢(Saiba como será as operações de Sorosgale, Gale e Ciclos)

🔣JUROS C.🔣(Calcule seu lucro baseado em juros compostos saiba como será o seu futuro seguindo gerenciamento)
'''

    MSG004 = "<b>🤖: Tudo certo {0},  só precisamos fazer esta etapa uma vez.\n segue a sugestão do bot caso queira iniciar.\n seu codigo para os comando é 🔐 {1} ainda sim não compartilhe🙄\n(Sua senha foi registrada com criptografia).</b>"

    MSG005 =  "<b>🤖: Sugestão: iniciar {0}, p ou  iniciar {0},r \n caso o comando não seja obedecido use um / na frente de iniciar.</b>"

    MSG006 =  "🤖: Email invalido ou não cadastrado. se acha estranho ou caso de erro contate o suporte😤😒🙄🙄🙄"
    
    MSG007 = 'Ok {0}.... pode ser que esteja alguma operação em andamento🧐\nAguarde os gales possivelmente 😁\nMasss se deseja pode vender as opeações na plataforma da IQ😜😜 só vai  aí vai encerrar\nEm caso de erro contate o suporte😤😒🙄🙄🙄'

    MSG008 = '{0}, está parando o que ja está parado❓ está doido❓ 🤨🤔\nEm caso de erro contate o suporte😤😒🙄'

    MSG009 = '<b>🤖 Ordem executada:\n💹 {0} 💶 {1}\n Ⓜ️{2}  🔃{3}\n</b>'

    MSG010 = "<html><head/><body><p>ENTRADA R${0}&nbsp;&nbsp;&nbsp;&nbsp;  <span style='color:lime'>🟢S.WIN: {17}&nbsp;&nbsp;&nbsp;&nbsp;</span> <span style='color:red'>🔴S.LOSS: {18}</span><br/><br/>INICIO -  Entrada R${19}<br/><br/><br/>NIVEL 1 - 1° Entrada R${1}<br/>NIVEL 1 - 2° Entrada R${2}<br/><br/>NIVEL 2 - 1° Entrada R${3}<br/>NIVEL 2 - 2° Entrada R${4}<br/><br/>NIVEL 3 - 1° Entrada R${5}<br/>NIVEL 3 - 2° Entrada R${6}<br/><br/>NIVEL 4 - 1° Entrada R${7}<br/>NIVEL 4 - 2° Entrada R${8}<br/><br/>NIVEL 5 - 1° Entrada R${9}<br/>NIVEL 5 - 2° Entrada R${10}<br/><br/>NIVEL 6 - 1° Entrada R${11}<br/>NIVEL 6 - 2° Entrada R${12}<br/><br/>NIVEL 7 - 1° Entrada R${13}<br/>NIVEL 7 - 2° Entrada R${14}<br/><br/>NIVEL 8 - 1° Entrada R${15}<br/>NIVEL 8 - 2° Entrada R${16} </p></body></html>"

    MSG011 ="<html><head/><body><p>ENTRADA R${0}&nbsp;&nbsp;&nbsp;&nbsp;  <span style='color:lime'>🟢S.WIN: {11}&nbsp;&nbsp;&nbsp;&nbsp;</span> <span style='color:red'>🔴S.LOSS: {12}</span><br/><br/>NIVEL 1 - Entrada  R${1}<br/>NIVEL 1 - G1  R${2}<br/><br/>NIVEL 2 - Entrada  R${3}<br/>NIVEL 2 - G1  R${4}<br/><br/>NIVEL 3 - Entrada R${5}<br/>NIVEL 3 - G1 R${6}<br/><br/>NIVEL 4 - Entrada R${7}<br/>NIVEL 4 - G1 R${8}<br/><br/>NIVEL 5 - Entrada R${9}<br/>NIVEL 5 - G1 R${10}<br/><br/></body></html>"

    MSG012 ="<html><head/><body><p>ENTRADA INICIAL R${0}&nbsp;&nbsp;&nbsp;&nbsp;  <span style='color:lime'>🟢S.WIN: {19}&nbsp;&nbsp;&nbsp;&nbsp;</span> <span style='color:red'>🔴S.LOSS: {20}</span><br/><br/>INICIAL - Entrada  R${1}<br/>INICIAL - G1  R${2}<br/>INICIAL - G2  R${3}<br/><br/>NIVEL 1 - Entrada  R${4}<br/>NIVEL 1 - G1  R${5}<br/>NIVEL 1 - G2  R${6}<br/><br/>NIVEL 2 - Entrada  R${7}<br/>NIVEL 2 - G1  R${8}<br/>NIVEL 2 - G2  R${9}<br/><br/>NIVEL 3 - Entrada R${10}<br/>NIVEL 3 - G1 R${11}<br/>NIVEL 3 - G2  R${12}<br/><br/>NIVEL 4 - Entrada R${13}<br/>NIVEL 4 - G1 R${14}<br/>NIVEL 4 - G2  R${15}<br/><br/>NIVEL 5 - Entrada R${16}<br/>NIVEL 5 - G1 R${17}<br/>NIVEL 5 - G2  R${18}<br/><br/></body></html>"

    MSG013 ="<html><head/><body><p>ENTRADA INICIAL R${0}&nbsp;&nbsp;&nbsp;&nbsp;  <span style='color:lime'>🟢S.WIN: {6}&nbsp;&nbsp;&nbsp;&nbsp;</span> <span style='color:red'>🔴S.LOSS: {7}</span><br/><br/>NIVEL 1 - Entrada  R${1}<br/><br/>NIVEL 2 - Entrada  R${2}<br/><br/>NIVEL 3 - Entrada R${3}<br/><br/>NIVEL 4 - Entrada R${4}<br/><br/>NIVEL 5 - Entrada R${5}<br/><br/></body></html>"

    MSG014 = "Não há lista para hoje ainda volte mais tarde🤨😁"
