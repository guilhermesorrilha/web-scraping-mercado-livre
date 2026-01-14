import requests
from bs4 import BeautifulSoup
import json
import re

item_escolha = "iphone 17" #input('Qual item do Mercado Livre você gostaria de consultar? ')
item_escolha = item_escolha.strip().lower()
item_escolha = item_escolha.replace(' ', '-')


lista_podutos = []


# PRIMEIRA PAGINA
url = f'https://lista.mercadolivre.com.br/{item_escolha}'
header = {
    'Connection': 'keep-alive',
    'device-memory': '8',
    'dpr': '1',
    'viewport-width': '1920',
    'rtt': '0',
    'downlink': '10',
    'ect': '4g',
    'sec-ch-ua': '"Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-ch-ua-platform-version': '19.0.0',
    'sec-ch-ua-model': '',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.mercadolivre.com.br/',
}
response_primeiro = requests.get(url=url, headers=header)
soup_primerio = BeautifulSoup(response_primeiro.text, 'html.parser')
# =================================================================


# JOGA TODOS OS ITENS DA PAGINA NA LISTA (lista_podutos)
for item in soup_primerio.find_all('li', class_='ui-search-layout__item'):
    lista_podutos.append(item)
# ==================================================================



# ACHA O JSON DENTRO DO HTML E PEGA OS LINKS DAS PROXIMAS PAGINAS
inicio = response_primeiro.text.find('>_n.ctx.r=')
final = response_primeiro.text.find('"currentSnackbar":null,"isEshopsEnvironment":false}},"mainEntry":"___search-index"}')
json = json.loads(response_primeiro.text[inicio + 10:final + 83])
lista_paginas = json['appProps']['pageProps']['initialState']['pagination']['pagination_nodes_url']
# ==================================================================



# PERCORRE PAGINA POR PAGINA E PEGA SEUS ITENS E JOGA DENTRO DA LISTA
for pagina in lista_paginas:
    if pagina['value'] == "1":
        continue

    print(pagina)

    url = pagina['url']
    response_demais_paginas = requests.get(url=url, headers=header)
    soup_demais_paginas = BeautifulSoup(response_demais_paginas.text, 'html.parser')

    for item in soup_demais_paginas.find_all('li', class_='ui-search-layout__item'):
        lista_podutos.append(item)
# ==================================================================




for posicao, produto in enumerate(lista_podutos):
    titulo = produto.find('h3', class_='poly-component__title-wrapper').text
    preco = produto.find('span', class_='andes-money-amount andes-money-amount--cents-superscript').text
    img = produto.find('img', class_='poly-component__picture')
    img_url = img.get('src')
    print(f'{titulo}\n{preco}\n{img_url}\n{'-'*75}')
    if posicao == 99:
        break


