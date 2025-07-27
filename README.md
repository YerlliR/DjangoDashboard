# 🚀 BitPy - Plataforma de Monitoreo de Criptoactivos

![BitPy Banner](https://img.shields.io/badge/BitPy-Crypto%20Portfolio-blue?style=for-the-badge&logo=bitcoin)

**BitPy** es una plataforma web de monitoreo y análisis de criptoactivos que proporciona información financiera en tiempo real del mercado cripto con capacidades de gestión de portafolios digitales.

## 📋 Tabla de Contenidos

- [✨ Características](#-características)
- [🛠️ Tecnologías](#️-tecnologías)
- [📦 Instalación](#-instalación)
- [🚀 Uso](#-uso)
- [📊 API y Datos](#-api-y-datos)
- [🔄 Automatización](#-automatización)
- [🗃️ Base de Datos](#️-base-de-datos)
- [🎨 Interfaz](#-interfaz)
- [🔮 Roadmap](#-roadmap)
- [🤝 Contribución](#-contribución)
- [📄 Licencia](#-licencia)

## ✨ Características

### 🌟 Funcionalidades Actuales

- **📈 Monitoreo en Tiempo Real**: Visualización de precios actuales de más de 1000 criptomonedas
- **💾 Base de Datos Histórica**: Almacenamiento local de todos los precios para análisis independiente
- **📊 Datos Propios**: Recopilación continua cada minuto para gráficos y análisis sin límites de API
- **🔍 Búsqueda Inteligente**: Buscar criptomonedas por nombre o símbolo
- **📊 Información Detallada**: 
  - Precio actual en USD
  - Market Cap
  - Estado de la moneda (activa/deprecated)
  - Última actualización
  - Logo de la criptomoneda
- **📱 Diseño Responsivo**: Interfaz optimizada para desktop y móvil
- **⚡ Paginación Eficiente**: Navegación fluida entre grandes volúmenes de datos
- **🎨 UI Moderna**: Diseño dark theme con efectos glassmorphism

### 🚧 En Desarrollo

- **👛 Gestión de Wallets**: Crear y administrar múltiples carteras digitales
- **💼 Portfolio Tracking**: Seguimiento de inversiones y rendimiento
- **📊 Price Simulator**: Simulador de precios y proyecciones
- **📈 Gráficos Históricos**: Visualización de tendencias de precio
- **🔔 Alertas de Precio**: Notificaciones personalizadas
- **📋 Reportes**: Generación de informes de rendimiento

## 🛠️ Tecnologías

### Backend
- **Framework**: Django 5.2.4
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Python**: 3.11+
- **ORM**: Django ORM

### Frontend
- **CSS Framework**: CSS Custom + Google Fonts (Inter)
- **Iconos**: Font Awesome 6.5.0
- **JavaScript**: Vanilla JS (futuras mejoras con React/Vue)

### APIs Externas
- **CoinGecko API**: Datos de criptomonedas en tiempo real
- **Rate Limiting**: 50 requests/minuto (plan gratuito)

### DevOps y Automatización
- **Cron Jobs**: Actualización automática de precios
- **Django Management Commands**: Comandos personalizados
- **Logging**: Sistema de logs estructurado

## 📦 Instalación

### Prerrequisitos
- Python 3.11 o superior
- pip
- Git

### 🚀 Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/bitpy-crypto-portfolio.git
cd bitpy-crypto-portfolio

# 2. Crear entorno virtual
python -m venv env
source env/bin/activate  # Linux/Mac
# env\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py makemigrations
python manage.py migrate

# 5. Cargar datos iniciales (opcional)
python manage.py update_crypto_prices --pages=2

# 6. Ejecutar servidor de desarrollo
python manage.py runserver
```

### 📋 Requirements.txt
```txt
Django==5.2.4
requests==2.31.0
python-decouple==3.8
```

## 🚀 Uso

### Servidor de Desarrollo
```bash
python manage.py runserver
```
Accede a http://localhost:8000

### Actualizar Datos de Criptomonedas
```bash
# Actualización manual
python manage.py update_crypto_prices --pages=4 --verbose

# Ver ayuda del comando
python manage.py update_crypto_prices --help
```

### Búsqueda de Criptomonedas
- Navega a la página principal
- Usa el buscador para filtrar por nombre o símbolo
- Utiliza la paginación para explorar todas las criptomonedas

## 📊 API y Datos

### Fuente de Datos
- **CoinGecko API**: https://api.coingecko.com/api/v3/
- **Endpoints utilizados**:
  - `/coins/markets`: Lista de criptomonedas con precios
  - Parámetros: `vs_currency=usd`, `order=market_cap_desc`

### Límites de Rate
- **Plan Gratuito**: 50 requests/minuto
- **Actualización configurada**: Cada 1 minuto
- **Páginas por actualización**: 4 (1000 criptomonedas)
- **Almacenamiento histórico**: Todos los datos se guardan localmente para análisis posteriores

## 🔄 Automatización

### Cron Job Configurado
```bash
# Actualización cada 1 minuto para máxima precisión
* * * * * cd /ruta/proyecto && python manage.py update_crypto_prices --pages=4 >> /var/log/crypto.log 2>&1
```

### Almacenamiento de Datos Históricos
- **Base de datos local**: Todos los precios se almacenan históricamente
- **Granularidad**: Datos cada minuto para análisis detallado
- **Uso futuro**: Generación de gráficos con datos propios sin depender de APIs externas
- **Ventajas**: 
  - Sin límites de consulta histórica
  - Datos siempre disponibles offline
  - Base para machine learning y predicciones
  - Generación de gráficos customizados

### Management Commands Disponibles
- `update_crypto_prices`: Actualiza precios desde CoinGecko
  - `--pages`: Número de páginas a procesar
  - `--verbose`: Información detallada
  - `--delay`: Tiempo entre requests

## 🗃️ Base de Datos

### Modelos Principales

```python
# Criptomoneda
class Crypto(models.Model):
    name = models.CharField(max_length=100)           # Bitcoin
    symbol = models.CharField(max_length=100)         # BTC
    logo = models.CharField(max_length=100)           # URL del logo
    deprecated = models.BooleanField()                # Estado

# Precio Histórico con Granularidad por Minuto
class Crypto_price(models.Model):
    crypto = models.ForeignKey(Crypto)
    date = models.DateField()                         # Fecha del precio
    price = models.FloatField()                       # Precio en USD
    market_cap = models.FloatField()                  # Capitalización
    
    # Nota: Cada registro representa un punto en el tiempo (cada minuto)
    # Esto permite análisis temporal detallado y gráficos de alta resolución

# Wallet del Usuario (En desarrollo)
class Wallet(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)

# Transacciones (En desarrollo)
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet)
    crypto = models.ForeignKey(Crypto)
    date = models.DateField()
    amount = models.FloatField()
```

### Relaciones
- Un `Crypto` puede tener múltiples `Crypto_price` (histórico)
- Un `User` puede tener múltiples `Wallet`
- Una `Wallet` puede tener múltiples `Transaction`

## 🎨 Interfaz

### Características del Diseño
- **🌙 Dark Theme**: Tema oscuro profesional
- **✨ Glassmorphism**: Efectos de cristal y blur
- **📱 Responsive**: Adaptable a todas las pantallas
- **🎨 Animaciones**: Transiciones suaves CSS
- **🔍 UX Optimizada**: Navegación intuitiva

### Componentes Principales
- **Navbar**: Navegación principal con logo
- **Search Bar**: Buscador con autocomplete visual
- **Crypto Table**: Tabla responsive con paginación
- **Pagination**: Navegación entre páginas de resultados

## 🔮 Roadmap

### Fase 1: MVP ✅ (Completado)
- [x] Estructura básica Django
- [x] Modelos de datos
- [x] Integración CoinGecko API
- [x] Vista de lista de criptomonedas
- [x] Búsqueda y paginación
- [x] Automatización con cron

### Fase 2: Portfolio Management 🚧 (En Desarrollo)
- [ ] Sistema de autenticación de usuarios
- [ ] CRUD de wallets personalizadas
- [ ] Registro de transacciones
- [ ] Dashboard de portfolio
- [ ] Cálculo de P&L (Profit & Loss)

### Fase 3: Analytics & Visualization 📊 (Planificado)
- [ ] Gráficos de precio histórico usando datos propios (Chart.js)
- [ ] Análisis temporal con granularidad por minuto
- [ ] Price Simulator con proyecciones basadas en datos históricos
- [ ] Análisis de rendimiento con datos reales almacenados
- [ ] Exportación de reportes (PDF/Excel) con gráficos personalizados
- [ ] Alertas de precio por email/SMS

### Fase 4: Advanced Features 🚀 (Futuro)
- [ ] API REST propia
- [ ] Integración con exchanges (Binance, Coinbase)
- [ ] Portfolio compartido/público
- [ ] Social features (seguir usuarios)
- [ ] Mobile App (React Native/Flutter)

## 🤝 Contribución

### Cómo Contribuir
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Estándares de Código
- Seguir PEP 8 para Python
- Comentarios en español para el código
- Tests unitarios para nuevas funcionalidades
- Documentación actualizada

### Areas de Contribución
- 🐛 **Bug Fixes**: Corrección de errores
- ✨ **Features**: Nuevas funcionalidades
- 📚 **Documentation**: Mejora de documentación
- 🎨 **UI/UX**: Mejoras de diseño
- ⚡ **Performance**: Optimizaciones

## 📈 Métricas del Proyecto

- **🗂️ Archivos**: ~20 archivos Python/HTML/CSS
- **📊 Modelos**: 4 modelos Django
- **🔗 APIs**: 1 integración externa (CoinGecko)
- **📱 Páginas**: 3 páginas principales
- **💾 Base de Datos**: ~1000+ registros de criptos
- **⏱️ Frecuencia de datos**: Cada minuto (1440 registros/día por crypto)
- **📈 Capacidad de análisis**: Datos históricos ilimitados para gráficos propios

## 🔧 Configuración Avanzada

### Variables de Entorno
```env
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
DATABASE_URL=postgresql://user:pass@localhost/bitpy_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configuración de Producción
- Usar PostgreSQL en lugar de SQLite
- Configurar Redis para cache
- Nginx como reverse proxy
- Gunicorn como WSGI server
- SSL/HTTPS habilitado

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Yerlli** - *Desarrollador Principal*
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## 🙏 Agradecimientos

- **CoinGecko** por proporcionar la API gratuita de datos crypto
- **Django Community** por el excelente framework
- **Font Awesome** por los iconos
- **Google Fonts** por la tipografía Inter

---

<div align="center">
  <p><strong>⭐ Si te gusta el proyecto, ¡dale una estrella!</strong></p>
  <p>Desarrollado con ❤️ para la comunidad crypto</p>
</div>
