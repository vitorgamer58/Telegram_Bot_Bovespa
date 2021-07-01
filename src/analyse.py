"""
Starting June 23rd, 2021, Chatbase will be in maintenance mode and we will no longer accept any new bots. All API calls in Chatbase Analytics will stop working after September 27th, 2021
"""

""" # coding: utf-8
# vitorgamer58
import requests
import json

api_key = 'YOUR_API_KEY_HERE'
url = 'https://chatbase-area120.appspot.com/api/message'


def send_menssage(funcao, type, mensagem, username):
    if type == 'user':
        mensagem = funcao + ' ' + mensagem

    headers = {'cache-control': 'no-cache',
               'content-type': 'application/json'}
    body = {
            "api_key": api_key,
            "type": type,
            "platform": "telegram",
            "message": mensagem,
            "intent": "Use",
            "version": "1.0",
            "user_id": username
          }
    
    resposta = requests.post(url, data = json.dumps(body), headers=headers)
    print('Envio ok')

def not_handled(type, mensagem, username):
    headers = {'cache-control': 'no-cache',
               'content-type': 'application/json'}
    body = {
            "api_key": api_key,
            "type": type,
            "platform": "telegram",
            "message": mensagem,
            "not_handled": "true",
            "intent": "use",
            "version": "1.0",
            "user_id": username
          }
    
    resposta = requests.post(url, data = json.dumps(body), headers=headers)
    print('Envio OK')
 """