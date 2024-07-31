import os
from pathlib import Path

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-01a^wc2kflvivde7%4j!*3n2090!-s)+21@k5g5ur4!=a)p#g8'
DEBUG = True
ALLOWED_HOSTS = ["*"]
APPEND_SLASH = False

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ckeditor',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',

    'apps.app',
    'apps.users',
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),

}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Internationalization
LANGUAGE_CODE = 'uz-ru'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # noqa

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

JAZZMIN_SETTINGS = {
    "site_title": "Smart-tizim ERP",
    "site_header": "Smart-tizim ERP",
    "site_brand": "Smart-tizim ERP",
    "site_logo": "path/to/logo.png",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to the Smart-tizim ERP superadmin panel",
    "copyright": "Acme Smart-tizim ERP Ltd",
    "search_model": ["auth.User"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://t.me/AzizbekGulomov", "new_window": True},
        {"model": "auth.User"},
        {"app": "apps"},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://t.me/AzizbekGulomov", "new_window": True},
        {"model": "auth.User"}
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app.Product": "fas fa-cube",
        "app.Category": "fas fa-tags",
        "app.Banner": "fas fa-image",
        "app.Order": "fas fa-map-marker-alt",
        "app.OrderItem": "fas fa-shopping-cart",
        "users.User": "fas fa-users",
        "users.Company": "fas fa-building",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_SECRET_KEY = 'sk_test_51O2EEvBJlouxhpbibHG4gUqjIlbo9SazFPvd31OkBpazbyQVNEgfoelcaCrKSFN1Ln5RlNEwGW0l4BvM5GIyrA6b009ZHvBvu0'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51O2EEvBJlouxhpbitwOhBgXbdslgiysOC4AcLN8S2JIByp7WRZYVbX1ajnlMbzs5V68wbtDHcggCfFbXb7YqoOXM00CvuF8RUo'
