# coding: utf-8
# vitorgamer58
import requests
import json

api_key = 'YOUR_API_KEY_HERE
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

# send_menssage('price', 'user', 'ROMI3', 'user-00')