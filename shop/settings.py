"""
Django settings for shop project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u^+!k+$$403u#(o-)b-l7fz%$y45i)eh+gth^&wdtnoeu*v%cx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'catalog.apps.CatalogConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'reviews.apps.ReviewsConfig',
    'wishlist.apps.WishlistConfig',
    'blog.apps.BlogConfig',
    'pages.apps.PagesConfig',
    'contacts.apps.ContactsConfig',
    'config.apps.ConfigConfig',
    'textpages.apps.TextpagesConfig',
    'textpages2.apps.Textpages2Config',
    'uploads.apps.UploadsConfig',
    'brands.apps.BrandsConfig',
    'easy_thumbnails',
    'django_quill',
    'metatags',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop.urls'

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
                'cart.context_processors.cart_processor',
                'cart.context_processors.add_to_cart_processor',
                'wishlist.context_processors.wishlist_processor',
                'catalog.context_processors.menu_catalog_processor',
                'catalog.context_processors.search_form',
                'catalog.context_processors.logos',
                'config.context_processors.main_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'itzone_db',
        'USER': 'itadmin',
        'PASSWORD': 'abc123!',
        'HOST': 'localhost'
    }
}
# sudo -i -u postgres
# psql itzone_db;

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Easy thumbnail settings
THUMBNAIL_ALIASES = {
    '': {
        'small': {'size': (150, 150), 'crop': False},
        'small-x2': {'size': (300, 300), 'crop': False},
        'medium': {'size': (900, 900), 'crop': False},
    },
}

# Cart Session
CART_SESSION_ID = 'cart'

# Wishlist Session
WISHLIST_SESSION_ID = 'wishlist'

# Max file upload memory size
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

SEND_MAIL_TO = 'sales@itzone.ru'

try:
    from .local_settings import *
except ImportError:
    pass

TITLE_SUFFIX = ' - IT.zone'
