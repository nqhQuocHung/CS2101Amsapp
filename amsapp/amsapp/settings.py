"""
Django settings for amsapp project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7@avyx(l_rnwr!91x$o@)m+nb*zg1)f8zla1u48p(6_+n4w*!d'

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
    'ams.apps.AmsConfig',
    'ckeditor',
    'ckeditor_uploader',
    'cloudinary',
    'rest_framework',
    'drf_yasg',
    'oauth2_provider',
    'corsheaders',

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'ams.middleware.LecturerPasswordChangeMiddleware',


]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}

ROOT_URLCONF = 'amsapp.urls'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hungmt2426@gmail.com'
EMAIL_HOST_PASSWORD = 'viohxnfiiuhsmysy'


import cloudinary
cloudinary.config(
    cloud_name="dcnvpuvq5",
    api_key="265516843643197",
    api_secret="m1WUuVl8sZ5aMubBmzLQ3fgXeSk"
)

import  pymysql
pymysql.install_as_MySQLdb()
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
PASSWORD_LECTURER_DEFAULT = 'ou@123'
WSGI_APPLICATION = 'amsapp.wsgi.application'
CKEDITOR_UPLOAD_PATH = "ckeditor/images/"
MEDIA_ROOT = '%s/ams/static/' % BASE_DIR
AUTH_USER_MODEL = 'ams.User'
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'amsdb',
        'USER': 'root',
        'PASSWORD': '2410Mythao.@',
        'HOST': ''  # mặc định localhost
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CLIENT_ID = 'jhD8Z2VwzubfUZmsWe4bdvehT0gFTNoaiyZaBNiF'
CLIENT_SECRET = 'H3LOa98ryAJ6SPtfclzi9WpU9xO9dosOj8JnCcGSc5Fjqc0Q3QNjvtTynYorKfIhLdwfI0ylWdja6FHyZ38sBiJijAvgzqN1gl1wwY3L5Js1IbQKNhZpEqzhLtJ6ZqNS'
