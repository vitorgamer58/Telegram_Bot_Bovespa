# Telegram_Bot_Bovespa
Este é o código Backend escrito em Python de um Bot do Telegram

## Instalação
abra /src/conf/.env.sample e digite o token do seu bot do telegram na linha 1 e o token do [Coinlib](https://coinlib.io/) na linha 4, salve com arquivo com o nome .env em vez de .env.sample e então na pasta raiz, digite os seguintes comandos:

    pip install -r requirements.txt
    python scr/core.py

E então rode o programa [phoemur](https://github.com/phoemur/fundamentus) disponibilizado como submódulo deste projeto, na pasta raiz deste digite:
    
    pip install -r required.txt
    python phoemur/fundamentos.py
    python phoemur/server.py

Várias funções do bot precisam que o arquivo server.py esteja rodando, pois é ele que responde com indicadores fundamentalistas baixados do site [fundamentus](https://fundamentus.com.br/)

## Funcionamento em Funções
A função principal do Bot é retornar a cotação de alguma ação listada na Bolsa de Valores B3, de acordo com a solicitação do usuário, a solicitação das cotações se dá através da API [mfinance](https://mfinance.com.br/swagger/index.html), a solicitação dos fundamentos atráves do programa phoemur, e o preço do bitcoin atráves da api da biscoint.
| Funções | Descrição |
|--|--|
| /price + código da ação | retorna a cotação e a variação no dia |
| /fii + código do fundo | retorna a cotação, a variação no dia e o dividend yield dos ultimos 12 meses de acordo com a cotação do dia
| /bitcoin	| retorna a cotação do bitcoin |
| /fundamentus + código da ação | retorna indicadores fundamentalistas
| /graham + código da ação | retorna o valor justo de acordo com a fórmula de Graham
| /fechamento | retorna as maiores altas e baixas do ibovespa

## Problemas e Bugs conhecidos
O bot pode retornar um erro no console ao usar o comando /fechamento, sendo o erro envolvendo o arquivo bovespa_indice2.csv - isso se dá por um problema envolvendo diferentes sistemas operacionais, foi constatado que este erro acontece no Linux, porém não no Windows.

Pode ser resolvido trazendo o arquivo bovespa_indice2.csv para dentro da pasta src e alterando o caminho na linha 30 do arquivo funcoes.py para 'bovespa_indice2.csv'


## Devidos créditos e direitos autorais de terceiros
O código base para a criação deste bot se deu por um tutorial postado no medium.com de autoria do Mauro de Carvalho, que pode ser encontrado aqui: [https://medium.com/](https://medium.com/@mdcg.dev/desenvolvendo-o-seu-primeiro-chatbot-no-telegram-com-python-a9ad787bdf6)

O código base encontra-se aqui: [/commit/a64fe47fb1b5f101ea68736c3099d9b7f9a08b67](https://github.com/vitorgamer58/Telegram_Bot_Bovespa/commit/a64fe47fb1b5f101ea68736c3099d9b7f9a08b67)

Para o preço do bitcoin usa-se a api do [Coinlib](https://coinlib.io/)

Alguns indicadores e o preço da ação derivam da API [mfinance](https://mfinance.com.br/swagger/index.html)

### Fundamentus
Utiliza-se o código [phoemur](https://github.com/phoemur/fundamentus) que puxa os dados do site [Fundamentus](https://fundamentus.com.br/) 

## Licença
Você é livre para usar, copiar, modificar, distribuir, fazer uso privado ou comercial, **desde que** dê os devidos créditos aos autores, de acordo com a [licença MIT](https://github.com/vitorgamer58/Telegram_Bot_Bovespa/blob/master/LICENSE).
