import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-01a^wc2kflvivde7%4j!*3n2090!-s)+21@k5g5ur4!=a)p#g8'
DEBUG = False
ALLOWED_HOSTS = ["api.tashkentmarket.ae","admin.tashkentmarket.ae"]
APPEND_SLASH = False
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my_apps
    'apps',
    'apps.orders',
    'apps.users',
    'apps.landing',

    # 3rd party apps
    'ckeditor',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',
    'corsheaders',

]

AUTH_USER_MODEL = 'users.User'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 800,
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://api.tashkentmarket.ae",
    "https://tashkentmarket.ae",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
SITE_URL = 'http://127.0.0.1:8000'
LANGUAGE_CODE = 'uz-ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # noqa

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


JAZZMIN_SETTINGS = {
    "site_title": "Tashkent-Marker ERP",
    "site_header": "Tashkent-Marker ERP",
    "site_brand": "Tashkent-Marker ERP",
    "site_logo": "assets/images/Tashkent Market.png",
    "login_logo": 'assets/images/logo_size.jpg',
    "login_logo_dark": "assets/images/logo_size.jpg",
    "site_logo_classes": "img-circle",
    "site_icon": 'assets/images/logo_size.jpg',
    "welcome_sign": "Welcome to the Tashkent-Marker ERP superadmin panel",
    "copyright": "Acme Tashkent-Marker ERP Ltd",
    "search_model": ["users.User"],
    "user_avatar": None,
    "navbar": "navbar-navy navbar-dark",

    "show_sidebar": True,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "orders.Product": "fas fa-cube",
        "orders.Category": "fas fa-tags",
        "orders.Banner": "fas fa-image",
        "orders.Order": "fas fa-map-marker-alt",
        "orders.OrderItem": "fas fa-shopping-cart",
        "users.User": "fas fa-users",
        "users.Company": "fas fa-building",

        "orders.DeliveryInfo": "fas fa-truck",
        "orders.PolicyAndPrivacy": "fas fa-file-alt",
        "orders.PublicOffer": "fas fa-handshake",
        "orders.ReturnPolicy": "fas fa-undo",
        "orders.OrderHistory": "fas fa-history",
        "orders.TelegramChannel": "fab fa-telegram-plane",

        "landing.SpecialOffer": "fas fa-gift",
        "landing.Company": "fas fa-building", 
        "landing.SocialNetworks": "fas fa-share-alt",  
        "landing.News": "fas fa-newspaper", 
        "landing.Recall": "fas fa-phone-alt", 
        "landing.AboutUs": "fas fa-info-circle",  
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"users.user": "collapsible", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-navy",
    "accent": "accent-primary",
    "navbar": "navbar-navy navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "footer": "sidebar-dark-navy",
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
        "language_chooser": True,
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic',
            'description': 'Phone number and password.'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Type in the *\'Value\'* input box below: **\'Bearer &lt;JWT&gt;\'**, '
                           'where JWT is the JSON web token you get back when logging in.'
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
