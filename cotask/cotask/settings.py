import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-ar01s&5_s$crk35dpcdg4bstrc6k=^2(#9tcf_vv%l@2stvj#h"

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "guest",
    "social_media",
    "remember_line",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = "cotask.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cotask.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "notification_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


TIME_ZONE = "UTC"

USE_TZ = True


USE_L10N = True



# STATIC_URL = "/static/"

# STATIC_ROOT = (BASE_DIR / 'static')

# STATICFILES_DIRS = [BASE_DIR / 'static']


# MEDIA_ROOT = (BASE_DIR / 'media')

# MEDIA_URL = '/media/'


#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URL для браузера
STATIC_URL = '/static/'

# Путь для сбора статики командой collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

# Директории с исходной статикой
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'templates', 'src'),
]

# Медиафайлы
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATIC_URL = '/static/'
# STATIC_ROOT = '/app/static'  # Должен совпадать с путем в Nginx
# STATICFILES_DIRS = ('/app/static',)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = '/app/media'


LOGOUT_REDIRECT_URL = "/"

LOGIN_REDIRECT_URL = 'feed'


LANGUAGE_CODE = 'ru'
USE_I18N = True

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1', 'https://ваш-домен.ru']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')