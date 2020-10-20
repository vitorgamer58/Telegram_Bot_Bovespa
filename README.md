# Telegram_Bot_Bovespa
Este é o código Backend escrito em Python de um Bot do Telegram

## Instalação
abra /src/conf/.env e digite o token do seu bot do telegram na linha 1 e então na pasta raiz, digite:

    pip install -r requirements.txt
    python scr/core.py

e então baixe o programa [phoemur](https://github.com/phoemur/fundamentus) e na pasta raiz deste digite

    python fundamentos.py

com os dois programas rodando, basta usar

## Funcionamento em Funções
A função principal do Bot é retornar a cotação de alguma ação listada na Bolsa de Valores B3, de acordo com a solicitação do usuário, a solicitação das cotações se dá através da API [mfinance](https://mfinance.com.br/swagger/index.html), a solicitação dos fundamentos atráves do programa phoemur, e o preço do bitcoin atráves da api da biscoint.
| Funções | Descrição |
|--|--|
| /price + código da ação | retorna a cotação e a variação no dia |
| /bitcoin	| retorna a cotação do bitcoin |
| /fundamentus + código da ação | retorna indicadores fundamentalistas

## Devidos créditos e direitos autorais de terceiros
O código base para a criação deste bot se deu por um tutorial postado no medium.com de autoria do Mauro de Carvalho, que pode ser encontrado aqui: [https://medium.com/](https://medium.com/@mdcg.dev/desenvolvendo-o-seu-primeiro-chatbot-no-telegram-com-python-a9ad787bdf6)

O código base encontra-se aqui: [/commit/a64fe47fb1b5f101ea68736c3099d9b7f9a08b67](https://github.com/vitorgamer58/Telegram_Bot_Bovespa/commit/a64fe47fb1b5f101ea68736c3099d9b7f9a08b67)

Para o preço do bitcoin usa-se a api da [Biscoint](https://biscoint.io/)

### Fundamentus
Utiliza-se o código [phoemur](https://github.com/phoemur/fundamentus) que puxa os dados do site [Fundamentus](https://fundamentus.com.br/) 

## Licença
Você é livre para usar, copiar, modificar, distribuir, fazer uso privado ou comercial, **desde que** dê os devidos créditos aos autores, de acordo com a [licença MIT](https://github.com/vitorgamer58/Telegram_Bot_Bovespa/blob/master/LICENSE).