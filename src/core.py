# coding: utf-8
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import requests
import os

from conf.settings import BASE_API_URL, TELEGRAM_TOKEN


def start(bot, update):
    response_message = "=^._.^="
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def http_cats(bot, update, args):
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
        bot.send_message(
            chat_id=update.message.chat_id,
            text=f"código {args[0]} não encontrado, tem certeza que está correto?")



def unknown(bot, update):
    response_message = "Não Entendi"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('price', http_cats, pass_args=True)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()