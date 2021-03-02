"""
Django settings for ecommerce_django project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import django_heroku
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0di2r@1o@sn#3r)zw_t-8@k^#%6dqpo$4hn_%wmdw13d@k31v_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_base.apps.AppBaseConfig',
    'stripe'
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
#
# MIDDLEWARE_CLASSES = (
#     # Simplified static file serving.
#     # https://warehouse.python.org/project/whitenoise/
#     'whitenoise.middleware.WhiteNoiseMiddleware',)
#
# # Simplified static file serving.
# # https://warehouse.python.org/project/whitenoise/
#
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'ecommerce_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_base.context_processors.menu_links',
                'app_base.context_processors.cart_infos',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "app_base_login"
LOGIN_REDIRECT_URL = "app_base_home"

STRIPE_PUBLISHABLE_KEY = 'pk_test_51HipXHK6qedgwkuuC5TcEzpg5exJz3FACbWH2SBdbQmpLtOAanU3FEzWbbFlGGV28tLioG16fUuYUUjeMFa8cgBT00j3CgigTn'
STRIPE_SECRET_KEY = 'sk_test_51HipXHK6qedgwkuudTU6M3dFDj7UlAinebUH2I4CKUGdx7yL1lt57gmfMkObnO8mmg4jlT5qkYKLXSAeozYKbyrD00igpVsA2Q'
STRIPE_ENDPOINT_SECRET = ''
SESSION_ENGINE = 'app_base.session_backend'

# Activate Django-Heroku.
django_heroku.settings(locals())
