import os
import environ
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(', ')

AUTH_USER_MODEL = 'account.CustomUser'

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

LANGUAGE_CODE = 'en'

USE_I18N = True

USE_L10N = True

LANGUAGES = [
    ('en', _('English')),
    ('pt-br', _('Brazilian Portuguese')),
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]

TIME_ZONE = 'UTC'

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(', ')

CORS_ALLOW_CREDENTIALS = bool(os.getenv('CORS_ALLOW_CREDENTIALS'))


CORS_ORIGIN_ALLOW_ALL = bool(os.getenv('CORS_ORIGIN_ALLOW_ALL'))

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "OPTIONS",
    "PUT",
    "PATCH",
    "DELETE",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
]

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # CORS
    'corsheaders',
    # Rest
    'rest_framework',
    'rest_framework_simplejwt',
    # Apps
    'apps.account'
]

MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    # Django
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom authentication
    'apps.account.backends.JWTAuthenticationMiddleware',
]

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

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE'),
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
        'OPTIONS': {
            'sslmode': 'verify-full',
            'sslrootcert': os.getenv('DB_CERTIFICADO'),
        },
    }
}

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=float(os.getenv('ACCESS_TOKEN_LIFETIME_MINUTES'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=float(os.getenv('REFRESH_TOKEN_LIFETIME_DAYS'))),
}
