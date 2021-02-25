from lbcapi import api
import re
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# START OF VARIABLES

# Search by currencies
currencies = ['CAD', 'USD']

# Payment Methods to search
payment_methods = ['payoneer', 'zelle', 'paypal', 'interac-e-transfer']

# Specific search by country and payment method
countries = [{
    'code': 'AR',
    'name': 'ARGENTINA',
    'currency': 'USD',
}]

# END OF VARIABLES

RAPID_API_SECRET_HOST = os.getenv("RAPID_API_SECRET_HOST")
RAPID_API_SECRET_KEY = os.getenv("RAPID_API_SECRET_KEY")

LOCAL_BTC_HMAC_KEY = os.getenv("LOCAL_BTC_HMAC_KEY")
LOCAL_BTC_HMAC_SECRET = os.getenv("LOCAL_BTC_HMAC_SECRET")

url = "https://perodriguezl-cryptocurrency-real-time-v1.p.rapidapi.com/info/BTC"

headers = {
    'x-rapidapi-host': RAPID_API_SECRET_HOST,
    'x-rapidapi-key': RAPID_API_SECRET_KEY
}

response = requests.request("GET", url, headers=headers)

value = response.json()

non_decimal = re.compile(r'[^\d.]+')

my_score = 99


def interate_over_ads(me_json):
    trade_count = {}
    i = 0
    global value
    for x in me_json['data']['ad_list']:
        price = float(x['data']['temp_price_usd'])
        reference = value['price_usd']
        rating = int(non_decimal.sub('', x['data']['profile']['trade_count']))
        score = int(x['data']['profile']['feedback_score'])
        if rating < 50 or score < 95 or x['data']['require_feedback_score'] > my_score:
            continue
        if i == 0:
            minimum = {
                'username': x['data']['profile']['username'],
                'rating': rating,
                'score': score,
                'reference_rapidapi': reference,
                'price': price,
                'ad': x['actions']['public_view'],
                'diff': str((price-reference)*100/price),
                'currency': x['data']['currency'],
                'method': x['data']['online_provider'],
                'require_feedback_score': x['data']['require_feedback_score'],
                'require_trade_volume': x['data']['require_trade_volume'],
            }
        else:
            if float(x['data']['temp_price_usd']) < minimum['price']:
                minimum = {
                    'username': x['data']['profile']['username'],
                    'rating': rating,
                    'score': score,
                    'reference_rapidapi': reference,
                    'price': price,
                    'ad': x['actions']['public_view'],
                    'diff': str((price-reference)*100/price),
                    'method': x['data']['online_provider'],
                    'currency': x['data']['currency'],
                    'require_feedback_score': x['data']['require_feedback_score'],
                    'require_trade_volume': x['data']['require_trade_volume'],
                }
        i = i + 1
    print(minimum)

conn = api.Connection()

print('by currency')
print(currencies)

for currency in currencies:
    me_json = requests.get('https://localbitcoins.com/buy-bitcoins-online/{}/.json'.format(currency)).json()
    interate_over_ads(me_json)

print('by payment methods')
print(payment_methods)

payment_methods_list = requests.get('https://localbitcoins.com/api/payment_methods/').json()

countries_list = requests.get('https://localbitcoins.com/api/countrycodes/').json()

currencies_list = requests.get('https://localbitcoins.com/api/currencies/').json()

for payment in payment_methods:
    me_json = requests.get('https://localbitcoins.com/buy-bitcoins-online/{}/.json'.format(payment)).json()
    interate_over_ads(me_json)

print(countries)

for country in countries:
    string = 'https://localbitcoins.com/buy-bitcoins-online/{}/{}/{}/.json'.format(country['code'], country['name'], 'national-bank-transfer')
    me_json = requests.get(string).json()
    for x in me_json['data']['ad_list']:
        if x['data']['currency'] != country['currency']:
            me_json['data']['ad_list'].remove(x)
    interate_over_ads(me_json)
