import requests
from datetime import datetime
from portafolioCripto.models import Crypto, Crypto_price

api_page = 1

while(api_page <= 4):

    enlace = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={api_page}&sparkline=false"
    respones = requests.get(enlace)

    data = respones.json()

    for crypto_json in data:

        if not Crypto.objects.filter(name=crypto_json['name']).exists():
            Crypto(
                name=crypto_json['name'], 
                symbol=crypto_json['symbol'].upper(), 
                logo=crypto_json['image'], 
                deprecated = False
            ).save()


        Crypto_price(
            price=crypto_json['current_price'], 
            date=datetime.now(), 
            crypto= Crypto.objects.get(name=crypto_json['name']),
            market_cap = crypto_json['market_cap']
        ).save()
        
    api_page += 1