from django.shortcuts import render, redirect
from .models import Crypto
from django.core.paginator import Paginator 
from django.db.models import Q 
from django.contrib.auth.models import User
from datetime import datetime 
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages





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


def wallet_view(request):

    return render(request, 'wallet.html', {

    })

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
        print("POST data:", request.POST)  # Para debug
        
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