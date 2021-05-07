# coding: utf-8
# vitorgamer58
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import requests
import os
from conf.settings import BASE_API_URL, TELEGRAM_TOKEN, BISCOINT, PHOEMUR
import logging
import math

#from pandas_datareader import data as wb
#import matplotlib.pyplot as plt
#import datetime

import operator
import csv

from datetime import date

logger = logging.getLogger()
logger.setLevel(logging.INFO)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def fechamento(bot, update):
    with open('./bovespa_indice2.csv', newline='') as f:
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

    bot.send_message(
        chat_id=update.message.chat_id,
        text='Confira os dados de fechamento do pregão!🦈'
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
        f'5️⃣ {maior_baixa[8]} {maior_baixa[9]}%')

    #Imprime no log
    string_log = "/Comando fechamento Acionado"
    logging.info(string_log)

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Olá, eu sou um robô, meus comandos são:"
        "\n"
        "/price + Código da ação (Responde com o valor da ação)"
        "\n"
        "/bitcoin (Responde com a cotação do bitcoin na biscoint)"
        "\n"
        "/fundamentus + Código da ação (Responde com o valor da ação)"
        "\n"
        "/graham + Código da ação (Responde com o preço justo segundo a fórmula de Graham)"
        "\n"
        "/fechamento (responde com as maiores altas e maiores baixas do ibov"
    )


def funpricestock(bot, update, args):
    if len(args) == 0:
        '''
        Esse IF verifica se o usuário não passou como argumento do comando
        Em caso positivo, envia a mensagem e dá um return para finalizar a função funpricestock
        '''
        bot.send_message(
            chat_id=update.message.chat.id,
            text="Você precisa informar o ticket da ação")
        return

    ticker = args[0].upper()
    busca = BASE_API_URL + "stocks/" + ticker
    json = requests.get(busca)

    if(json.status_code == 200):
        json = json.json()
        priceaction = json['lastPrice']
        changeaction = json['change']
        symbol = json['symbol']

        if priceaction == 0:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Código {ticker} não encontrado, tem certeza que está correto?")
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"O preço da ação {symbol} é: R$ {priceaction} sendo a variação no dia de {changeaction}%")

        string_log = f"Comando /price acionado - {symbol}, {priceaction}"
        logging.info(string_log)

    else:

        if(json.status_code == 404):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Código {args[0]} não encontrado, tem certeza que está correto?")
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="O servidor das cotações está indisponível no momento")


def funbitcoin(bot, update):
    buscabtc = BISCOINT
    jsonbtc = requests.get(buscabtc)
    if(jsonbtc.status_code == 200):
        jsonbtc = jsonbtc.json()
        pricebtc = jsonbtc['data']['last']
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"O preço do Bitcoin é R$ {pricebtc}")
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Sistema temporariamente indisponível")


def fundamentus(bot, update, args):
    if len(args) == 0:
        bot.send_message(
            chat_id=update.message.chat.id,
            text="Você precisa informar o ticket da ação")
        return

    busca = PHOEMUR
    ticker = args[0].upper()
    busca1 = requests.get(busca)
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
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f"FUNDAMENTUS {ticker}"
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
        f"ROIC: {roic}%"
    )


def grahamprice(ticker):
    busca = BASE_API_URL + "stocks/" + ticker
    json = requests.get(busca)
    json = json.json()
    price = json['lastPrice']
    return price


def graham(bot, update, args):
    if len(args) == 0:
        bot.send_message(
            chat_id=update.message.chat.id,
            text="Você precisa informar o ticket da ação")
        return

    ticker = args[0].upper()
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

            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"O preço justo da ação {ticker} segundo a fórmula de Graham é: R$ {graham}"
                "\n"
                f"Com um {resultado} de {abs(desconto_agio)}%"
                "\n"
                f"Preço: {price}  VPA: {vpa}  LPA: {lpa}")
            string_log = f"{ticker}, {vpa}, {lpa}"
            logging.info(string_log)
        else:
            if(vpa < 0):
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text="VPA menor que zero, não é possível calcular!"
                    "\n"
                    f"VPA: {vpa}  LPA: {lpa}")

            elif(lpa < 0):
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text="LPA menor que zero, não é possível calcular!"                    "\n"
                    f"VPA: {vpa}  LPA: {lpa}")

            elif(vpa == 0):
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text=f"API mfinance está fora do ar ou o código {ticker} é inválido.")

    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="A API mfinance está indisponível no momento por um motivo desconhecido.")


'''
def grafico(bot, update, args):
    ticker = args[0].upper()
    ticker = ticker + '.SA'
    start = datetime.datetime(2018, 1, 1)
    end = datetime.datetime(2021, 5, 1)
    data = wb.DataReader(ticker, data_source='yahoo', start=start, end=end)
    print(data.tail())
    data['Close'].plot(figsize=(8, 5))
    plt.savefig('./graph.png')
    bot.send_photo(
        chat_id=update.message.chat_id,
        photo=open('./graph.png', 'rb')
    )
    if os.path.exists('./graph.png'):
        os.remove('./graph.png')
'''


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Não Entendi"
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=False)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('price', funpricestock, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('bitcoin', funbitcoin, pass_args=False)
    )
    dispatcher.add_handler(
        CommandHandler('fundamentus', fundamentus, pass_args=True)
    )
    dispatcher.add_handler(
        CommandHandler('graham', graham, pass_args=True)
    )
    '''dispatcher.add_handler(
        CommandHandler('grafico', grafico, pass_args=True)
    )'''
    dispatcher.add_handler(
        CommandHandler('fechamento', fechamento, pass_args=False)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
