from django.core.management.base import BaseCommand
import requests
from datetime import datetime
from django.utils import timezone  # ← Importar timezone de Django
from portafolioCripto.models import Crypto, Crypto_price
from django.conf import settings


class Command(BaseCommand):

    help = 'Actualizar precios de criptomonedas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=4,
            help='Número de páginas a procesar (default: 4)'
        )
        
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostrar información detallada'
        )

    def handle(self, *args, **options):

        api_pages = options['pages']
        verbose = options['verbose']
        
        self.stdout.write(
            self.style.SUCCESS(f'Iniciando actualización ({api_pages} páginas)... - {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')
        )

        total_processed = 0
        
        for api_page in range(1, api_pages + 1):
            if verbose:
                self.stdout.write(f'Procesando página {api_page}...')
                
            try:
                base_url = settings.COINGECKO_API_BASE
                endpoint = settings.COINGECKO_MARKETS_ENDPOINT
                enlace = f"{base_url}{endpoint}?vs_currency=usd&order=market_cap_desc&per_page=250&page={api_page}&sparkline=false"

                response = requests.get(enlace, timeout=30)
                response.raise_for_status()
                
                data = response.json()

                # Obtener la fecha/hora actual con timezone una sola vez por página
                current_time = timezone.now()

                for crypto_json in data:
                    try:
                        # Crear o actualizar crypto
                        crypto, created = Crypto.objects.get_or_create(
                            name=crypto_json['name'],
                            defaults={
                                'symbol': crypto_json['symbol'].upper(),
                                'logo': crypto_json['image'],
                                'deprecated': False
                            }
                        )
                        
                        if not created:
                            crypto.symbol = crypto_json['symbol'].upper()
                            crypto.logo = crypto_json['image']
                            crypto.save()

                        # Crear precio con timezone-aware datetime
                        Crypto_price.objects.create(
                            price=crypto_json['current_price'],
                            date=current_time,  # ← Usar timezone.now() directamente
                            crypto=crypto,
                            market_cap=crypto_json.get('market_cap')
                        )
                        
                        total_processed += 1
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error: {crypto_json.get("name", "unknown")}: {e}')
                        )
                        
                if verbose:
                    self.stdout.write(f'✓ Página {api_page} completada')
                    
            except requests.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(f'Error de conexión en página {api_page}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'✓ Completado! {total_processed} criptos procesadas')
        )