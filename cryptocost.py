import requests
import json

def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def all_cryptos_usd():
    url_ = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    j = requests.get(url_)
    data = json.loads(j.text)
    return {i['symbol']: i['current_price'] for i in data}


def get_price_usd(crypto_input):
    a = all_cryptos_usd()
    for i in crypto_input:
        if i in a:
            return a[i]

def all_cryptos_rub():
    url_ = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=rub&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    j = requests.get(url_)
    data = json.loads(j.text)
    return {i['symbol']: i['current_price'] for i in data}


def get_price_rub(crypto_input):
    a = all_cryptos_rub()
    for i in crypto_input:
        if i in a:
            return a[i]