from django.shortcuts import render, redirect
from .models import Crypto, Transaction, Wallet
from django.core.paginator import Paginator 
from django.db.models import Q 
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
import json
from typing import cast

def probar_404(request):
    raise Http404("Forzando error 404 para probar la plantilla")

def index_view(request):

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

@login_required
def wallet_detail_view(request, wallet_id):

    user_crypto_list = []

    # obtener usuario del request
    user = request.user

    # FILTRO PARA EVITAR ACCEDER A WALLETS QUE NO SEAN DEL USUARIO
    wallet = Wallet.objects.get(
        user = user, 
        id = wallet_id
    )

    transactions = list(Transaction.objects.filter(wallet=wallet))

    for transaction in transactions:

        transacion_crypto = transaction.crypto
        latest_price = transaction.crypto.crypto_price_set.order_by('-date').first() # type: ignore
        index = next(
            (i for i, user_crypto in enumerate(user_crypto_list) if user_crypto["crypto_name"] == transacion_crypto.name),
            None
        )

        if index is None:
            
            user_crypto_list.append(
                
                {
                    "crypto_name": transacion_crypto.name, 
                    "crypto_symbol": transacion_crypto.symbol, 
                    "crypto_logo": transacion_crypto.logo, 
                    "crypto_price": latest_price.price,  # type: ignore
                    "amount": transaction.amount, 
                    "medium_price": transaction.buy_price,
                    "quantity_transactions": 1,
                    "value": transaction.amount * latest_price.price, # type: ignore
                    "profit": transaction.amount * latest_price.price - transaction.amount * transaction.buy_price,
                    "percentage_profit": round((latest_price.price - transaction.buy_price) / transaction.buy_price * 100, 2)
                }
                
            )
        else:

            user_crypto_list[index]["quantity_transactions"] += 1
            user_crypto_list[index]["amount"] += transaction.amount
            user_crypto_list[index]["medium_price"] = (user_crypto_list[index]["medium_price"] + transaction.buy_price) / user_crypto_list[index]["quantity_transactions"]
            user_crypto_list[index]["value"] += transaction.amount * latest_price.price # type: ignore
            user_crypto_list[index]["profit"] += transaction.amount * latest_price.price - transaction.amount * transaction.buy_price
            user_crypto_list[index]["percentage_profit"] = round((latest_price.price - transaction.buy_price + user_crypto_list[index]["medium_price"]) / (transaction.buy_price + user_crypto_list[index]["medium_price"]) * 100, 2)


    crypto_list = list(Crypto.objects.all())

    if request.method == 'POST':

        crypto_selected = Crypto.objects.get(
            id = int(request.POST['crypto_select'])
        )

        Transaction.objects.create(
            wallet = wallet,
            crypto = crypto_selected,
            date = request.POST['date'],
            amount = request.POST['amount'],
            buy_price = request.POST['price']
        )
    
    return render(request, 'wallet_detail.html', {
        'crypto_list': crypto_list,
        'wallet': wallet,
        'user_crypto_list': user_crypto_list
    })


@login_required
def wallet_list_view(request):

    user = request.user
    wallet_list = list(Wallet.objects.filter(user=user))

    return render(request, 'wallet_list.html', {
        'wallet_list': wallet_list
    })

@login_required
@csrf_protect
def wallet_create_view(request):

    if request.method == 'POST':

        try:
            walletConfig = json.loads(request.body)

            name = walletConfig.get('name', '').strip()
            color = walletConfig.get('color', '').strip()
            icon = walletConfig.get('icon', '').strip()

            Wallet.objects.create(
                user = request.user,
                name = name,
                icon = icon,
                color = color
            )

            # Envia respuesta al fectch para que redirija al wallet_list al estar completada con exito la operacion
            return JsonResponse({'success': True, 'redirect_url': '/wallet/'}) 

        except Exception as e:
            print(e)

            # el redirect_url aqui ahora mismo no se esta usando 
            return JsonResponse({'success': False, 'redirect_url': '/wallet/create-new/'}) 

    # Si no recibe POST carga la plantilla de creacion
    return render(request, 'wallet_create.html')


def login_view(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html', {
                    'error': 'Credenciales incorrectas'
                })
        except User.DoesNotExist:

            return render(request, 'login.html', {
                'error': 'El usuario no existe'
            })

    return render(request, 'login.html', {

    })

@csrf_protect
def signup_view(request):

    if request.method == 'POST':     
        # Obtener datos del formulario
        name = request.POST.get('name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')

        # Validaciones
        if not name:
            return render(request, 'signup.html', {
                'error': 'El nombre es requerido'
            })
        
        if not last_name:
            return render(request, 'signup.html', {
                'error': 'El apellido es requerido'
            })
        
        if not email:
            return render(request, 'signup.html', {
                'error': 'El email es requerido'
            })
        
        if len(password) < 6:
            return render(request, 'signup.html', {
                'error': 'La contraseña debe tener al menos 6 caracteres'
            })

        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Las contraseñas no coinciden'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {
                'error': 'El correo electrónico ya está registrado'
            })

        try:
            # Crear el usuario
            user = User.objects.create_user(
                username=email, 
                email=email,
                password=password,
                first_name=name,
                last_name=last_name
            )

            # Autenticar y loguear automáticamente al usuario
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'¡Bienvenido {name}! Tu cuenta ha sido creada exitosamente.')
                return redirect('index')  
            else:
                messages.error(request, 'Error al autenticar. Intenta iniciar sesión.')
                return redirect('login')  
                
        except Exception as e:
            return render(request, 'signup.html', {
                'error': 'Error al crear la cuenta. Intenta de nuevo.'
            })

    # Si es GET, mostrar el formulario vacío
    return render(request, 'signup.html')