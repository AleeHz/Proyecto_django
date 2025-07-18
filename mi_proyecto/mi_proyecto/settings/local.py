
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2klk3shw$h16!ef-mbw$)v6as$*v03c#n+g(^1i9wn)p%9m^wv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []





# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mi_pagina_django',
        'USER': 'root',
        'PASSWORD': '42745406ale1',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
