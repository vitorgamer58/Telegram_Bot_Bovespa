# coding: utf-8
# vitorgamer58
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from conf.settings import TELEGRAM_TOKEN
import logging
from funcoes import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def fechamento(update, context):
    call_function = get_fechamento(update.message.from_user['username'])
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=call_function['message']
    )


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Bem vindo {update.message.from_user['first_name']}, eu sou um robô e meus comandos são:"
        "\n"
        "/price + Código da ação (Responde com o valor da ação)"
        "\n"
        "/bitcoin (Responde com a cotação do bitcoin)"
        "\n"
        "/fundamentus + Código da ação (Responde com o valor da ação)"
        "\n"
        "/graham + Código da ação (Responde com o preço justo segundo a fórmula de Graham)"
        "\n"
        "/fechamento (responde com as maiores altas e maiores baixas do ibov"
    )


def price(update, context):
    call_function = get_price(
        context.args, update.message.from_user['username'])
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=call_function['message']
    )


def bitcoin(update, context):
    call_function = get_bitcoin(update.message.from_user['username'])
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=call_function['message'],
        parse_mode='Markdown'
    )


def fundamentus(update, context):
    call_function = get_fundamentus(
        context.args, update.message.from_user['username'])
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=call_function['message']
    )


def graham(update, context):
    call_function = get_graham(
        context.args, update.message.from_user['username'])
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=call_function['message']
    )


def fii(update, context):
    call_function = get_fii(context.args, update.message.from_user['username'])
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=call_function['message']
    )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Não Entendi"
    )


def sobre(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=("Este é um bot Open-Source, cujo código fonte está disponível no [Github](https://github.com/vitorgamer58/Telegram_Bot_Bovespa)"
              "\n"
              f"Criado por [vitorgamer58](tg://user?id=409733392) e está licenciado sob licença MIT"
              "\n"
              "Siga-me nas redes sociais: [Youtube](https://www.youtube.com/channel/UCn00U9AApstVzfJpFD9ALEA) e [Instagram](https://www.instagram.com/investimentosdovitor/)"
              "\n"
              "Em meu [Linktree](https://linktr.ee/investimentosdovitor) você pode encontrar mais links úteis, como cursos de investimento e corretoras de Bitcoin"),
        parse_mode="Markdown"
    )


def cripto(update, context):
    call_function = get_cripto(context.args)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=call_function['message'],
        parse_mode='Markdown'
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        CommandHandler('start', start, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('price', price, pass_args=True, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('bitcoin', bitcoin, pass_args=False, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('fundamentus', fundamentus,
                       pass_args=True, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('graham', graham, pass_args=True, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('fechamento', fechamento,
                       pass_args=False, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('fii', fii, pass_args=True, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('cripto', cripto, pass_args=True, run_async=True)
    )
    dispatcher.add_handler(
        CommandHandler('sobre', sobre, pass_args=False, run_async=True)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
