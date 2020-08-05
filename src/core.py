# coding: utf-8
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import requests
import os
from conf.settings import BASE_API_URL, TELEGRAM_TOKEN, BISCOINT

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Olá, eu sou um robô, meus comandos são:"
        "\n"
        "/price + Código da ação (Responde com o valor da ação)"
        "/bitcoin (responde com a cotação do bitcoin na biscoint)"
    )

def funpricestock(bot, update, args):
    busca = BASE_API_URL + args[0]
    json = requests.get(busca)
    if(json.status_code==200):
        json = json.json()
        priceaction = json['lastPrice']
        changeaction = json['change']
        symbol = json['symbol']
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"O preço da ação {symbol} é: {priceaction}, sendo a variação no dia de {changeaction}%")
    else:
        if(json.status_code==404):
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
        jsonbtc = jsonbtc.json()
        pricebtc = jsonbtc['data']['last']
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"O preço do Bitcoin é R$ {pricebtc}"
        )

def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Não Entendi"
    )

def main():
    updater = Updater(token=TELEGRAM_TOKEN)
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
        MessageHandler(Filters.command, unknown)
    )
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()