from django.shortcuts import render
from .models import Crypto, Crypto_price
import requests
from datetime import datetime
from django.core.paginator import Paginator 
from django.db.models import Q  


def index(request):

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
    
    ui_page = request.GET.get('page', 1)
    ui_search = request.GET.get('search', '')


    crypto_list = Crypto.objects.all()


    if ui_search:
        crypto_list = crypto_list.filter(
            Q(name__icontains=ui_search) | 
            Q(symbol__icontains=ui_search)
        )

    paginator = Paginator(crypto_list, 50)

    page_obj = paginator.get_page(ui_page)


    return render(request, 'index.html', {
        'page_obj': page_obj,
        'search_query': ui_search, 
        'total_cryptos': paginator.count, 
        })