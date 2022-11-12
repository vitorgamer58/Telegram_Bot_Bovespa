# coding: utf-8
# vitorgamer58

# from analyse import not_handled, #send_menssage
import requests
import logging
import math
import operator
from datetime import date

from conf.settings import BASE_API_URL, PHOEMUR, COINLIB, OKANE
import operator
from mongodb import *

from datetime import date

logger = logging.getLogger()
logger.setLevel(logging.INFO)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

default_headers = {"user-agent": "telegram-bot-bovespa/1.3.0",
                   "Content-Type": "application/json;charset=UTF-8"}

database = databaseClient()

def dontHaveArguments(ticker):
    if len(ticker) == 0: return True
    else: return False

def get_fechamento():
    # Puxa os dados de todas as empresas listadas
    data_stocks = requests.get(
        'https://mfinance.com.br/api/v1/stocks', headers=default_headers)
    if(data_stocks.status_code != 200):
        return {'status': 503,
                'message': "O servidor das cotações está indisponível no momento"}
    data_stocks = data_stocks.json()

    list_ibov = ["ALPA4","ABEV3","AMER3","ASAI3","AZUL4","B3SA3","BIDI11","BPAN4","BBSE3","BRML3","BBDC3","BBDC4","BRAP4","BBAS3","BRKM5","BRFS3","BPAC11","CRFB3","CCRO3","CMIG4","CIEL3","COGN3","CPLE6","CSAN3","CPFE3","CMIN3","CVCB3","CYRE3","DXCO3","ECOR3","ELET3","ELET6","EMBR3","ENBR3","ENGI11","ENEV3","EGIE3","EQTL3","EZTC3","FLRY3","GGBR4","GOAU4","GOLL4","NTCO3","SOMA3","HAPV3","HYPE3","IGTI11","GNDI3","IRBR3","ITSA4","ITUB4","JBSS3","JHSF3","KLBN11","RENT3","LCAM3","LWSA3","LAME4","LREN3","MGLU3","MRFG3","CASH3","BEEF3","MRVE3","MULT3","PCAR3","PETR3","PETR4","PRIO3","PETZ3","POSI3","QUAL3","RADL3","RDOR3","RAIL3","SBSP3","SANB11","CSNA3","SULA11","SUZB3","TAEE11","VIVT3","TIMS3","TOTS3","UGPA3","USIM5","VALE3","VIIA3","VBBR3","WEGE3","YDUQ3", "RRRP3"]

    # obter variação do indice Ibovespa
    ibov = [i for i in data_stocks['stocks']
            if (i['symbol'] in 'IBOV')]
    ibov = ibov[0]['change']

    # organiza pela alteração no dia - itemgetter('change')
    data_stocks['stocks'].sort(key=operator.itemgetter('change'))

    # Filtra as ações listadas, excluindo todas que não fazem parte do indice Ibovespa
    data_stocks = [i for i in data_stocks['stocks']
                   if (i['symbol'] in list_ibov)]
    quantidade_dados = len(data_stocks)  # conta a quantidade de dicts na lista

    # obter maiores altas
    quantidade_dados -= 1
    maior_alta = [data_stocks[quantidade_dados]['symbol'],
                  data_stocks[quantidade_dados]['change']]

    x = 5
    while x >= 1:
        x -= 1
        quantidade_dados -= 1
        maior_alta.append(data_stocks[quantidade_dados]['symbol'])
        maior_alta.append(data_stocks[quantidade_dados]['change'])
        # adiciona mais 4 empresas na lista de maiores altas

    # obter maiores baixas
    quantidade_dados = 0
    maior_baixa = [data_stocks[quantidade_dados]['symbol'],
                   data_stocks[quantidade_dados]['change']]

    y = 0
    while y <= 3:
        y += 1
        quantidade_dados += 1
        maior_baixa.append(data_stocks[quantidade_dados]['symbol'])
        maior_baixa.append(data_stocks[quantidade_dados]['change'])

    # obtem o dia de hoje
    data_atual = date.today()
    data_em_texto = data_atual.strftime('%d/%m/%Y')

    # obtem as mais negociadas
    data_stocks.sort(key=operator.itemgetter('volume'))  # organiza pelo volume
    quantidade_dados = len(data_stocks)
    quantidade_dados -= 1

    mais_negociadas = [data_stocks[quantidade_dados]['symbol'],
                       data_stocks[quantidade_dados]['change']]

    x = 5
    while x >= 1:
        x -= 1
        quantidade_dados -= 1
        mais_negociadas.append(data_stocks[quantidade_dados]['symbol'])
        mais_negociadas.append(data_stocks[quantidade_dados]['change'])
        # adiciona mais 4 empresas na lista de mais negociadas

    string_de_retorno = ('Confira os dados de fechamento do pregão!🦈'
                         "\n"
                         "\n"
                         f' {data_em_texto}'
                         "\n"
                         "\n"
                         f' 🇧🇷 IBOVESPA : {ibov}%'
                         "\n"
                         "\n"
                         '📈 MAIORES ALTAS DO IBOV'
                         "\n"
                         f'1️⃣ {maior_alta[0]} {maior_alta[1]}%'
                         "\n"
                         f'2️⃣ {maior_alta[2]} {maior_alta[3]}%'
                         "\n"
                         f'3️⃣ {maior_alta[4]} {maior_alta[5]}%'
                         "\n"
                         f'4️⃣ {maior_alta[6]} {maior_alta[7]}%'
                         "\n"
                         f'5️⃣ {maior_alta[8]} {maior_alta[9]}%'
                         "\n"
                         "\n"
                         '📉MAIORES BAIXAS DO IBOV'
                         "\n"
                         f'1️⃣ {maior_baixa[0]} {maior_baixa[1]}%'
                         "\n"
                         f'2️⃣ {maior_baixa[2]} {maior_baixa[3]}%'
                         "\n"
                         f'3️⃣ {maior_baixa[4]} {maior_baixa[5]}%'
                         "\n"
                         f'4️⃣ {maior_baixa[6]} {maior_baixa[7]}%'
                         "\n"
                         f'5️⃣ {maior_baixa[8]} {maior_baixa[9]}%'
                         "\n"
                         "\n"
                         '💥MAIS NEGOCIADAS DO PREGÃO'
                         "\n"
                         f'1️⃣ {mais_negociadas[0]} {mais_negociadas[1]}%'
                         "\n"
                         f'2️⃣ {mais_negociadas[2]} {mais_negociadas[3]}%'
                         "\n"
                         f'3️⃣ {mais_negociadas[4]} {mais_negociadas[5]}%'
                         "\n"
                         f'4️⃣ {mais_negociadas[6]} {mais_negociadas[7]}%'
                         "\n"
                         f'5️⃣ {mais_negociadas[8]} {mais_negociadas[9]}%')

    # Imprime no log
    string_log = "/Comando fechamento Acionado"
    logging.info(string_log)

    return {'status': 200,
            'message': string_de_retorno}

def get_price(ticker, username):
    if(dontHaveArguments(ticker)): return {'message': 'Você precisa informar o ticket da ação'}

    ticker = ticker[0].upper()
    # send_menssage('/price', 'user', ticker, username)
    busca = BASE_API_URL + "stocks/" + ticker
    json = requests.get(busca, headers=default_headers)

    if(json.status_code == 200):
        json = json.json()
        priceaction = json['lastPrice']
        changeaction = json['change']
        symbol = json['symbol']
        string_log = f"Comando /price acionado - {symbol}, {priceaction}"
        logging.info(string_log)

        if priceaction == 0:
            return {'status': 404,
                    'message': f"Código {ticker} não encontrado, tem certeza que está correto?"}
        else:
            return {'status': 200,
                    'message': f"O preço da ação {symbol} é: R$ {priceaction} sendo a variação no dia de {changeaction}%"}

    else:

        if(json.status_code == 404):
            return {'status': 404,
                    'message': f"Código {ticker} não encontrado, tem certeza que está correto?"}

        else:
            return {'status': 503,
                    'message': "O servidor das cotações está indisponível no momento"}

def get_bitcoin(username):
    string_log = "Comando /Bitcoin Acionado"
    logging.info(string_log)

    buscabtc = f'https://coinlib.io/api/v1/coin?key={COINLIB}&pref=BRL&symbol=BTC'
    jsonbtc = requests.get(buscabtc, headers=default_headers)
    if(jsonbtc.status_code == 200):
        jsonbtc = jsonbtc.json()
        if(jsonbtc['remaining'] > 0):
            pricebtc = round(float(jsonbtc['price']), 2)
            price_btc_usdt = round(float(jsonbtc['markets'][1]['price']), 2)
            # float transforma a string em número de ponto flutuante
            # round arredonda para duas casas decimais
            return {'status': 200,
                    'message': (f"O preço do Bitcoin é R$ {pricebtc}"
                                "\n"
                                f"Ou US$ {price_btc_usdt}"
                                "\n"
                                "Com dados do Coinlib.io"
                                "\n"
                                "Compre Bitcoins pela [Bitpreço](https://bitpreco.com/?r=26758)")}

        else:
            return {'status': 200,
                    'message': "API do Coinlib chegou ao máximo de solicitações, tente novamente mais tarde."}

    else:
        return {'status': 503,
                'message': "Sistema temporariamente indisponível"}

def get_fundamentus(ticker, username):
    if(dontHaveArguments(ticker)): return {'message': 'Você precisa informar o ticket da ação'}

    busca = PHOEMUR
    ticker = ticker[0].upper()
    # send_menssage('/Fundamentus', 'user', ticker, username)
    busca1 = requests.get(busca, headers=default_headers)
    if (busca1.status_code == 200):
        busca1 = busca1.json()
        cotacao = busca1[ticker]['Cotacao']
        # função ROUND faz com que o numero só tenha 2 casas decimais
        DY = round(((busca1[ticker]['DY'])*100), 2)
        div_brut_pat = round(((busca1[ticker]['Div.Brut/Pat.'])*100), 2)
        ev_ebit = busca1[ticker]['EV/EBIT']
        ev_ebitda = busca1[ticker]['EV/EBITDA']
        liq_corrente = busca1[ticker]['Liq.Corr.']
        mrg_ebit = round(((busca1[ticker]['Mrg.Ebit'])*100), 2)
        mrg_liq = round(((busca1[ticker]['Mrg.Liq.'])*100), 2)
        p_acl = busca1[ticker]['P/ACL']
        p_ativos = busca1[ticker]['P/Ativo']
        p_cap_giro = busca1[ticker]['P/Cap.Giro']
        p_ebit = busca1[ticker]['P/EBIT']
        p_l = busca1[ticker]['P/L']
        p_vp = busca1[ticker]['P/VP']
        psr = busca1[ticker]['PSR']
        roe = round(((busca1[ticker]['ROE'])*100), 2)
        roic = round(((busca1[ticker]['ROIC'])*100), 2)

        string_de_retorno = (f"FUNDAMENTUS {ticker}"
                             "\n"
                             f"Cotação no Fundamentus: {cotacao}"
                             "\n"
                             f"Dividend Yield: {DY}%"
                             "\n"
                             f"Dívida bruta / Patrimônio Líquido: {div_brut_pat}%"
                             "\n"
                             f"Margem EBIT: {mrg_ebit}%"
                             "\n"
                             f"Margem líquida: {mrg_liq}%"
                             "\n"
                             f"Valor da firma / EBIT: {ev_ebit}"
                             "\n"
                             f"Valor da firma / EBITDA: {ev_ebitda}"
                             "\n"
                             f"Liquidez corrente: {liq_corrente}"
                             "\n"
                             f"Preço / Ativo circulante líquido: {p_acl}"
                             "\n"
                             f"Preço / Ativos: {p_ativos}"
                             "\n"
                             f"Preço / Capital de giro: {p_cap_giro}"
                             "\n"
                             f"Preço / EBIT: {p_ebit}"
                             "\n"
                             f"Preço / Lucro: {p_l}"
                             "\n"
                             f"Preço / Valor Patrimonial: {p_vp}"
                             "\n"
                             f"Price Sales Ratio: {psr}"
                             "\n"
                             f"ROE: {roe}%"
                             "\n"
                             f"ROIC: {roic}%")

        return {'status': 200,
                'message': string_de_retorno}
    else:
        return {'status': 503,
                'message': 'O sistema está fora do ar por um motivo desconhecido'}

def get_graham(ticker, username):

    def calculaPrecoJusto(vpa, lpa):
        return round(math.sqrt(22.5 * lpa * vpa), 2)

    def stock_price(ticker):
        busca = BASE_API_URL + "stocks/" + ticker
        json = requests.get(busca, headers=default_headers)
        if(json.status_code != 200):
            return 0

        json = json.json()
        price = json['lastPrice']
        return price

    def returnMessage(vpa, lpa, ticker):
        graham = calculaPrecoJusto(vpa, lpa)
        price = stock_price(ticker)
        if (price == 0):
            return "Sistema indisponível no momento"

        desconto_agio = round(((price/graham)-1)*100, 2)

        if(desconto_agio <= 0):
            resultado = 'desconto'
        else:
            resultado = 'ágio'

        string_de_retorno = (f"O preço justo da ação {ticker} segundo a fórmula de Graham é: R$ {graham}"
                             "\n"
                             f"Com um {resultado} de {abs(desconto_agio)}%"
                             "\n"
                             f"Preço: {price}  VPA: {vpa}  LPA: {lpa}")
        return string_de_retorno

    def get_graham_okanebox(ticker):
        busca = OKANE + ticker
        requisicao = requests.get(busca, headers=default_headers)
        if(requisicao.status_code == 200):
            json = requisicao.json()
            lista = ['LPA', 'VPA']
            vpa_lpa = [i for i in json
                       if (i['title'] in lista)]
            lpa = round(vpa_lpa[0]['value'], 2)
            vpa = round(vpa_lpa[1]['value'], 2)
            # round arredonda para duas casas decimais
            if (vpa > 0 and lpa > 0):
                string_de_retorno = returnMessage(vpa, lpa, ticker)

            elif(vpa < 0):
                string_de_retorno = ("VPA menor que zero, não é possível calcular!"
                                     "\n"
                                     f"VPA: {vpa}  LPA: {lpa}")

            elif(lpa < 0):
                string_de_retorno = ("LPA menor que zero, não é possível calcular!"
                                     "\n"
                                     f"VPA: {vpa}  LPA: {lpa}")

        elif(requisicao.status_code == 404 or requisicao.status_code == 500):
            string_de_retorno = f'O ativo {ticker} não foi encontrado'

        else:
            string_de_retorno = 'Os servidores mfinance e okanebox estão fora do ar'

        string_de_retorno += ('\n''Fonte: OkaneBox')
        return string_de_retorno

    if(dontHaveArguments(ticker)): return {'message': 'Você precisa informar o ticket da ação'}

    ticker = ticker[0].upper()
    # send_menssage('/graham', 'user', ticker, username)
    graham_url = BASE_API_URL + "stocks/indicators/" + ticker
    json = requests.get(graham_url, headers=default_headers)
    if(json.status_code == 200):
        json = json.json()
        vpa = json['bookValuePerShare']['value']
        lpa = json['earningsPerShare']['value']
        if (vpa > 0 and lpa > 0):
            string_de_retorno = returnMessage(vpa, lpa, ticker)
            string_de_retorno += ('\n''Fonte: mfinance')
            var_return = {'status': 200,
                          'message': string_de_retorno}

        else:
            if(vpa < 0):
                string_de_retorno = ("VPA menor que zero, não é possível calcular!"
                                     "\n"
                                     f"VPA: {vpa}  LPA: {lpa}")

                var_return = {'status': 200,
                              'message': string_de_retorno}

            elif(lpa < 0):
                string_de_retorno = ("LPA menor que zero, não é possível calcular!"
                                     "\n"
                                     f"VPA: {vpa}  LPA: {lpa}")

                var_return = {'status': 200,
                              'message': string_de_retorno}

            elif(vpa == 0 and lpa == 0):
                # Caso a API mfinance esteja fora do ar...
                # Chama a API OkaneBox
                string_de_retorno = get_graham_okanebox(ticker)
                var_return = {'status': 200,
                              'message': string_de_retorno}

    else:
        # Caso a API mfinance esteja fora do ar...
        # Chama a API OkaneBox
        get_graham_okanebox(ticker)
        string_de_retorno = get_graham_okanebox(ticker)
        var_return = {'status': 200,
                      'message': string_de_retorno}

    string_log = f"Comando /graham acionado, {ticker}"
    logging.info(string_log)

    # send_menssage('/graham', 'agent', var_return['message'], username)
    return var_return

def get_fii(ticker, username):
    if(dontHaveArguments(ticker)): return {'message': 'Você precisa informar o ticket da ação'}

    # Faz a requisição dos dados para a API
    ticker = ticker[0].upper()
    get_fii = requests.get(
            'https://mfinance.com.br/api/v1/fiis/'+ticker, headers=default_headers)
    get_dividendos = requests.get(
            'https://mfinance.com.br/api/v1/fiis/dividends/'+ticker, headers=default_headers)

    if get_fii.status_code == 200 and get_dividendos.status_code == 200:
        # Transforma em Json e possibilita tratar os dados
        get_fii = get_fii.json()
        get_dividendos = get_dividendos.json()

        if get_fii['lastPrice'] != 0 and get_dividendos['dividends'] != None:
            """
            Verifica se o preço e o dividendo são diferentes de zero, pois a API mfinance
            Costuma responder com 200 informando valores zerados quando se solicita um código
            que não existe.
            """
            # Somar os 12 ultimos dividendos
            dividendos = 0
            soma_dividendos = 0

            '''
            Alguns fundos não possuem histórico com mais de 12 meses, necessita de uma estrutra if
            para evitar o erro list index out of range
            '''

            if len(get_dividendos['dividends']) < 12:
                ciclos = len(get_dividendos)-1
                # Conta a quantidade e reduz em 1
            else:
                ciclos = 11
                # São 12 meses, começando do zero até o onze, resultando em 12

            while dividendos <= ciclos:
                # print(dividendos)
                soma_dividendos = soma_dividendos + \
                    get_dividendos['dividends'][dividendos]['value']
                # Var dividendos indica a posição do valor no dict
                dividendos += 1

            # Arredonda 2 casas decimais
            soma_dividendos = round(soma_dividendos, 2)

            # Calcula o dividend yield
            dividend_yield = (soma_dividendos /
                                get_fii['closingPrice'])*100
            round(dividend_yield, 2)  # Arredonda

            string_de_retorno = (f"O preço do FII {ticker} é: R$ {get_fii['closingPrice']} sendo a variação no dia de {get_fii['change']}%"
                                    '\n'
                                    f'Neste preço, o dividend yield (12m) é de {round(dividend_yield, 2)}% com uma distribuição de R$ {round(soma_dividendos, 2)}')
            return {'status': 200, 'message': string_de_retorno}
        else:
            """
            Caso algum dos valores seja zero, necessita um tratamento especial para identificar o fato.
            """
            if get_fii['closingPrice'] == 0 and get_dividendos['dividends'] == None:
                # Não encontrado na API, provavelmente este FII não existe
                var_return = {
                    'status': 404, 'message': f'O fundo {ticker} não foi encontrado na API, tem certeza que digitou corretamente?'}
            elif get_fii['closingPrice'] != 0 and get_dividendos['dividends'] == None:
                string_de_retorno = (f"O preço do FII {ticker} é: R$ {get_fii['closingPrice']} sendo a variação no dia de {get_fii['change']}%"
                                        '\n'
                                        'Ainda não foi encontrado um histórico de dividendos para este fundo, ele pode ser muito novo.')
                return {'status': 200, 'message': string_de_retorno}
            else:
                return {'status': 500,
                                'message': 'erro desconhecido'}
    else:
        return {
            'status': 503, 'message': f'A API mfinance está fora do ar por um motivo desconhecido, erro {get_fii.status_code}'}

def get_cripto(ticker):
    if(dontHaveArguments(ticker)): return {'message': 'Você precisa informar o ticket da criptomoeda'}

    string_log = f"Comando /Coin {ticker} Acionado"
    logging.info(string_log)

    ticker = ticker[0].upper()
    buscacripto = f'https://coinlib.io/api/v1/coin?key={COINLIB}&pref=BRL&symbol={ticker}'
    jsoncripto = requests.get(buscacripto, headers=default_headers)
    if(jsoncripto.status_code == 200):
        jsoncripto = jsoncripto.json()
        if(jsoncripto['remaining'] > 0):
            pricecripto = round(float(jsoncripto['price']), 2)
            # price_cripto_usdt = round(float(jsoncripto['markets'][1]['price']), 2)
            # float transforma a string em número de ponto flutuante
            # round arredonda para duas casas decimais
            return {'status': 200,
                            'message': (f"O preço é R$ {pricecripto}"
                                        "\n"
                                        "Com dados do Coinlib.io")}
        else:
            return {'status': 200,
                            'message': "API do Coinlib chegou ao máximo de solicitações, tente novamente mais tarde."}

    else:
        return {'status': 503,
                        'message': "Sistema temporariamente indisponível"}

def cadastrar_fechamento(chat):
    result = database.addTelegramClient(chat)
    
    if(result):
        return "Cadastrado com sucesso"
    else:
        return "Provavelmente você já está cadastrado"

def descadastrar_fechamento(chat_id):
    result = database.removeTelegramClient(chat_id)
    if(result):
        return "Descadastrado com sucesso"
    else:
        return "Algum erro ocorreu"

def get_all_clients():
    clients = database.getAllClients()
    return clients