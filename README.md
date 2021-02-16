# localbitcoin.com-and-reference-API
This is a project for a script to run the calculations over validations for cripto currencies

## First setup your environment
- Create `.env` file locally.
- Copy all the content of `.env.example` file into `.env` file
- Fill `.env` file with the following variables:
```bash
RAPID_API_SECRET_HOST= <<RAPID API SECRETS>>
RAPID_API_SECRET_KEY= <<RAPID API SECRETS>>
LOCAL_BTC_HMAC_KEY= <<Localbitcoin.com Secrets>>
LOCAL_BTC_HMAC_SECRET= <<Localbitcoin.com Secrets>>
```

RAPID API SECRETS from: 
https://rapidapi.com/perodriguezl/api/cryptocurrency-real-time-bitcoin-ethereum-ripple-stellar-litecoin


## Install Dependencies

`pip install requirements.txt`

## Change the parameters as needed:

in `app.py` change as needed:

```python
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
```

## ENJOY ;)

run the script: `python app.py`