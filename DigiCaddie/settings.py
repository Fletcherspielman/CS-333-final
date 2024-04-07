"""
Django settings for DigiCaddie project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import django_heroku 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
USE_S3 = os.getenv('USE_S3') == 'TRUE'
# SECURITY WARNING: keep the secret key used in production secret!
if USE_S3:
    SECRET_KEY = os.getenv("SECRET_KEY")  
    SECURE_SSL_REDIRECT = True
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 15768000
else:
    SECRET_KEY = 'django-insecure-a6@2i3$6sh^63d9m664mma@112)xs@7o7b79p*75$p-6-vpy5o'
    DEBUG = False
    # ^nwz!y=%4&@n_u)kkgfh$ylavyk2lnag=&idw^4-y^slzxls3(
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['digicaddie.net', '127.0.0.1', '.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    #'round.apps.RoundConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'login',
    'main_page',
    'round',
    'django_bootstrap_icons',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'DigiCaddie.urls'

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

WSGI_APPLICATION = 'DigiCaddie.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# aws setting for database
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ciba',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = 'mediafiles/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static')


STORAGES = {
    # Enable WhiteNoise's GZip and Brotli compression of static assets:
    # https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'digicaddie@gmail.com'
EMAIL_HOST_PASSWORD = 'yljw nwra njum xfqo'

if 'MAPBOX_KEY' in os.environ:
    MAPBOX_KEY = os.getenv("MAPBOX_KEY")
else:
    MAPBOX_KEY = "pk.eyJ1IjoiZmxldGNoZXItc3BpZWxtYW4iLCJhIjoiY2xxMDRtbTZ5MHhoeDJqcDc5MTVtb2dmNyJ9.zjxU8lkUrl85cHdbntag5g"


SUPER_USER_PASSWORD = os.getenv("SUPER_USER_PASS")
AWS_CLIENT_KEY_ID = os.getenv("SECRET_CLIENT_KEY_REKOG") 
AWS_SECRET_ACCESS_KEY= os.getenv("SECRET_CLIENT_ACCESS_KEY_REKOG") 


django_heroku.settings(locals()) 