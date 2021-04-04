"""
Django settings for lipafair project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o27e1-&cn1td3v9tn430t_ft%engv8$6h%=ec#)ek3(=g7e+z*'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

PROD = False

if PROD:
    ALLOWED_HOSTS = ['.herokuapp.com']
else:
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'api',
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

ROOT_URLCONF = 'lipafair.urls'

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

WSGI_APPLICATION = 'lipafair.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if PROD:
    DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ORIGIN_ALLOW_ALL = True

MPESA_CONSUMER_SANDBOX = 'X2UxjtUhIeGh6DCXyYQfb9yBQGl101KY'

MPESA_SECRET_SANDBOX = '8iGGzslk7fuwvslQ'

MPESA_ENV = 'sandbox'

B2C_INITIATOR_PASSWORD = "APItest2950#"

B2C_SANDBOX_CALLBACK_URL = 'http://lipafair.herokuapp.com/api/withdraw-from-wallet-callback/'

B2C_SANDBOX_TIMEOUT_URL = 'http://lipafair.herokuapp.com/api/withdraw-from-wallet-callback/'

B2C_SANDBOX_INITIATOR_NAME = 'apiop70'

B2C_SANDBOX_PAYBILL = "602950"

MPESA_SHORT_CODE_SANDBOX = 174379
MPESA_SHORT_CODE_LIVE = None

MPESA_B2C_TEST_MSISDN = "254708374149"

LNM_PASSKEY_SANDBOX = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

MPESA_SANBOX_PASSWORD = 'QTcLhF7RyITHbtrEdyEZU3S/h/Vs0p0aYbW8nNIz8V/P4O23IL1xu/3E0BgbBOFihTJ7HtlPLbEeGObQGMrAxXlfr83ux/m/dCIa//uSLBF+WbEJ+os3Ryt/NkvGxKknXwUdfiQlo9RS7pFseZD8pZT4z8fFEA+ruFrbxvJQ8pZRsDuJ0VfEk+IeB+/GAdWSbE6mvDRvODMdZ6+1CMTxQ91EtA70eM3S3paalbfd33wFE0OxG8zb5o4nNJjmLWsklMyKIr8tcaQHo/ZqJykPjlYiSoIzXvAu/ZJar6xnkOTfo/njZINHY56dlT4pDX19ekCm4si+daylzSxRKAN9dw=='

FIREBASE_FUNC_USERNAME = "brian123@gmail.com"

FIREBASE_FUNC_PASSWORD = "134567"

FIREBASE_FUNC_AUTH_URL = "https://us-central1-lipa-fare-c7c76.cloudfunctions.net/api/login"

UPDATE_STORE_WALLET_ENDPOINT = "https://us-central1-lipa-fare-c7c76.cloudfunctions.net/api/update-wallet"

STORE_WALLET_URL = "https://us-central1-lipa-fare-c7c76.cloudfunctions.net/api/wallet/"

COUPON_CODE_LENGTH = 8

TARIFF_URL = 'https://us-central1-lipa-fare-c7c76.cloudfunctions.net/api/tariffs'