from django.shortcuts import render
from .models import Crypto
from django.core.paginator import Paginator 
from django.db.models import Q  


def index(request):

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


def wallet(request):

    return render(request, 'index.html', {

    })


def login(request):

    return render(request, 'login.html', {
        
    })