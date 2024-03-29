"""
Django settings for Websitegenerator project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4ko^6x&x(!-vzs^ehj$iduld85pucz@iycalk5k*ykqn^_$n%c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['softbit-website-builder.onrender.com']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DynamicGenerator',
    'social_django',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_bootstrap5',
    'django_htmx',
     
]

 
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Softbit.com",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Softbit Freelancer",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Softbit Freelancer",

    # Logo to use for your site, must be present in static files, used for brand on top left
    
    

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark":True,
}
JAZZMIN_SETTINGS["show_ui_builder"] = True
JAZZMIN_UI_TWEAKS = {
    
    "theme": "darkly",
}

 
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     
    'django_htmx.middleware.HtmxMiddleware',
    
]

ROOT_URLCONF = 'Websitegenerator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /"templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]
AUTHENTICATION_BACKENDS = (
     
     
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
     
    'social_core.backends.google.GoogleOAuth2',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '191238887921-kd039pfr42s27q30i0nog847nlojeidc.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

WSGI_APPLICATION = 'Websitegenerator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# settings.py

STRIPE_PUBLIC_KEY  = 'pk_test_51NaWhJJQmh7tshf7UBjp671cyquBm44eQwmq9viZu0MEWyxK3f0HDLrTi6RT3LS5E5vjF8kPgNCzmtzmdY2cSFLn00MVfxIY9r'
STRIPE_SECRET_KEY = 'sk_test_51NaWhJJQmh7tshf7PIGDbhCSEKypRH8l8P3mxMKcMde3zGtlQZEXyY8M1D74Unj7JyfmuBXfUPqMliSNvaBUJN1e00f2a8011D'
import os
from django.contrib.messages import constants as messages
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"static")
    
]
STATIC_ROOT=os.path.join(BASE_DIR,'assests')
MEDIA_URL ='/media/'
MEDIA_ROOT =os.path.join(BASE_DIR,"media")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MESSAGE_TAGS={
    messages.ERROR:'danger'
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shoaib4311859@gmail.com'
EMAIL_HOST_PASSWORD = 'wofegltuqmpfafkl'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
 

#CLIENT_ID='191238887921-kd039pfr42s27q30i0nog847nlojeidc.apps.googleusercontent.com'
#client_secret='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'