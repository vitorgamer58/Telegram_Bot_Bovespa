# coding: utf-8
# vitorgamer58

from src.analyse import not_handled, send_menssage
import requests
import logging
import math
import operator
import csv
from datetime import date

from conf.settings import BASE_API_URL, TELEGRAM_TOKEN, BISCOINT, PHOEMUR
import operator
import csv

from datetime import date

from analyse import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_fechamento(username):
    with open('../bovespa_indice2.csv', newline='') as f:
        reader = csv.reader(f)
        list_ibov = list(reader)
        # obtem uma lista de ações do indice IBOVESPA

    # Puxa os dados de todas as empresas listadas
    data_stocks = requests.get('https://mfinance.com.br/api/v1/stocks')
    data_stocks = data_stocks.json()

    # obter variação do indice Ibovespa
    ibov = data_stocks['stocks'][0]['change']

    # organiza pela alteração no dia - itemgetter('change')
    data_stocks['stocks'].sort(key=operator.itemgetter('change'))

    # Filtra as ações listadas, excluindo todas que não fazem parte do indice Ibovespa
    data_stocks = [i for i in data_stocks['stocks']
                   if (i['symbol'] in list_ibov[0])]
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
    
    send_menssage('/fechamento', 'agent', string_de_retorno, username)

    # Imprime no log
    string_log = "/Comando fechamento Acionado"
    logging.info(string_log)

    var_return = {'status': 'OK',
                    'message': string_de_retorno}
    
    return var_return

    
    



def get_price(ticker, username):
    if len(ticker) == 0:
        '''
        Esse IF verifica se o usuário não passou como argumento do comando
        Em caso positivo, envia a mensagem e dá um return para finalizar a função
        '''

        var_return = {'status': 'Empyt',
                    'message': 'Você precisa informar o ticket da ação'}
        not_handled('user', '/price', username)
        not_handled('agent', var_return['message'], username)
        return var_return


    ticker = ticker[0].upper()
    send_menssage('/price', 'user', ticker, username)
    busca = BASE_API_URL + "stocks/" + ticker
    json = requests.get(busca)

    if(json.status_code == 200):
        json = json.json()
        priceaction = json['lastPrice']
        changeaction = json['change']
        symbol = json['symbol']

        if priceaction == 0:
            var_return = {'status': '404',
            'message': f"Código {ticker} não encontrado, tem certeza que está correto?"}
        else:
            var_return = {'status': '200',
            'message': f"O preço da ação {symbol} é: R$ {priceaction} sendo a variação no dia de {changeaction}%"}

        string_log = f"Comando /price acionado - {symbol}, {priceaction}"
        logging.info(string_log)

    else:

        if(json.status_code == 404):
            var_return = {'status': '404',
            'message': f"Código {ticker} não encontrado, tem certeza que está correto?"}

        else:
            var_return = {'status': '0',
            'message': "O servidor das cotações está indisponível no momento"}
    
    send_menssage('/price', 'agent', var_return['message'], username)

    return var_return


def get_bitcoin(username):
    send_menssage('/bitcoin', 'user', '', username)
    buscabtc = BISCOINT
    jsonbtc = requests.get(buscabtc)
    if(jsonbtc.status_code == 200):
        jsonbtc = jsonbtc.json()
        pricebtc = jsonbtc['data']['last']
        var_return = {'status': '200',
        'message': f"O preço do Bitcoin é R$ {pricebtc}"}
    else:
        var_return = {'status': '0',
        'message': "Sistema temporariamente indisponível"}
    
    string_log = "Comando /Bitcoin Acionado"
    logging.info(string_log)

    send_menssage('/bitcoin', 'agent', var_return['message'], username)
    
    return var_return
    


def get_fundamentus(ticker, username):
    if len(ticker) == 0:
        var_return = {'status': '0',
        'message': "Você precisa informar o ticket da ação"}
        not_handled('user', '/fundamentus', username)
        not_handled('agent', var_return['message'], username)
        return var_return

    busca = PHOEMUR
    ticker = ticker[0].upper()
    send_menssage('/Fundamentus', 'user', ticker, username)
    busca1 = requests.get(busca)
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

        var_return = {'status': '200',
        'message': string_de_retorno}
    else:
        var_return = {'status': '0',
        'message': 'O sistema está fora do ar por um motivo desconhecido'}

    send_menssage('/Fundamentus', 'agent', var_return['message'], username)
    return var_return


def get_graham(ticker, username):

    def grahamprice(ticker):
        busca = BASE_API_URL + "stocks/" + ticker
        json = requests.get(busca)
        json = json.json()
        price = json['lastPrice']
        return price

    if len(ticker) == 0:
        var_return = {'status': '0',
        'message': "Você precisa informar o ticket da ação"}
        not_handled('user', '/graham', username)
        not_handled('agent', var_return['message'], username)
        return var_return

    ticker = ticker[0].upper()
    send_menssage('/Graham', 'user', ticker, username)
    graham_url = BASE_API_URL + "stocks/indicators/" + ticker
    json = requests.get(graham_url)
    if(json.status_code == 200):
        json = json.json()
        vpa = json['bookValuePerShare']['value']
        lpa = json['earningsPerShare']['value']
        if (vpa > 0 and lpa > 0):
            graham = round(math.sqrt(22.5 * lpa * vpa), 2)
            price = grahamprice(ticker)
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
            
            var_return = {'status': '200',
            'message': string_de_retorno}

        else:
            if(vpa < 0):
                string_de_retorno = ("VPA menor que zero, não é possível calcular!"
                    "\n"
                    f"VPA: {vpa}  LPA: {lpa}")

                var_return = {'status': '0',
                'message': string_de_retorno}

            elif(lpa < 0):
                    string_de_retorno = ("LPA menor que zero, não é possível calcular!"
                    "\n"
                    f"VPA: {vpa}  LPA: {lpa}")
                    
                    var_return = {'status': '0',
                    'message': string_de_retorno}


            elif(vpa == 0 and lpa == 0):
                var_return = {'status': '0',
                'message': f"API mfinance está fora do ar ou o código {ticker} é inválido."}

    else:
        var_return = {'status': '0',
                'message': "A API mfinance está indisponível no momento por um motivo desconhecido."}
    
    string_log = f"{ticker}, {vpa}, {lpa}"
    logging.info(string_log)
    
    send_menssage('/Graham', 'agent', var_return['message'], username)
    return var_return


