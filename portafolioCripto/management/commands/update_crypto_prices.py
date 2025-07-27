# portafolioCripto/management/commands/update_crypto_prices.py

from django.core.management.base import BaseCommand  # ← Clase base obligatoria
import requests
from datetime import datetime
from portafolioCripto.models import Crypto, Crypto_price

class Command(BaseCommand):  # ← DEBE llamarse "Command"
    # Descripción que aparece cuando haces --help
    help = 'Actualiza los precios de las criptomonedas desde CoinGecko API'

    def add_arguments(self, parser):
        """
        Aquí defines argumentos de línea de comandos personalizados
        Similar a argparse de Python
        """
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
        """
        MÉTODO PRINCIPAL - Aquí va tu lógica
        Django llama automáticamente a este método
        """
        # Obtener argumentos pasados
        api_pages = options['pages']
        verbose = options['verbose']
        
        # Usar self.stdout para imprimir (mejor que print)
        self.stdout.write(
            self.style.SUCCESS(f'Iniciando actualización ({api_pages} páginas)...')
        )

        total_processed = 0
        
        for api_page in range(1, api_pages + 1):
            if verbose:
                self.stdout.write(f'Procesando página {api_page}...')
                
            try:
                # Tu lógica original aquí
                enlace = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page={api_page}&sparkline=false"
                response = requests.get(enlace, timeout=30)
                response.raise_for_status()
                
                data = response.json()

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

                        # Crear precio
                        Crypto_price.objects.create(
                            price=crypto_json['current_price'],
                            date=datetime.now(),
                            crypto=crypto,
                            market_cap=crypto_json.get('market_cap')
                        )
                        
                        total_processed += 1
                        
                    except Exception as e:
                        # Manejo de errores con colores
                        self.stdout.write(
                            self.style.ERROR(f'Error: {crypto_json.get("name", "unknown")}: {e}')
                        )
                        
                if verbose:
                    self.stdout.write(f'✓ Página {api_page} completada')
                    
            except requests.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(f'Error de conexión en página {api_page}: {e}')
                )

        # Mensaje final con estilo
        self.stdout.write(
            self.style.SUCCESS(f'✓ Completado! {total_processed} criptos procesadas')
        )