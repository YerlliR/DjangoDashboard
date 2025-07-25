from django.shortcuts import render
from .models import Crypto, Crypto_price
import requests
from datetime import datetime

# Create your views here.
def index(request):

    respones = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false')

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
        


    crypto_list = list(Crypto.objects.all())

    return render(request, 'index.html', {
        'crypto_list': crypto_list
        })