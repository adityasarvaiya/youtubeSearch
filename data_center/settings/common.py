"""
Django settings for data_center project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import json
import os
from sys import path

from configurations import Configuration

from .celery import CelerySettingsMixin
from .constance import LiveSettingsMixin
from .logger import LoggerSettingsMixin


class Settings(CelerySettingsMixin, LoggerSettingsMixin, LiveSettingsMixin, Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Add our project to our python path, this way we don't need to type our project
    # name in our dotted import paths:
    path.append(BASE_DIR)

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get("SECRET_KEY", "")

    ALLOWED_HOSTS = []


    # App Configuration
    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_filters',
        'storages',
    ]

    HEALTH_CHECK_APPS = [
        'health_check',  # required
        'health_check.db',                          # stock Django health checkers
        'health_check.cache',
        'health_check.contrib.redis'
    ]

    # For HealthCheck
    REDIS_URL = f"redis://{os.environ.get('CACHE_LOCATION') or '127.0.0.1:6379/1'}"

    THIRD_PARTY_APPS = [
        'psqlextra',
        'safedelete',
        'rest_framework',
        'drf_yasg',
        'django_json_widget',
        'django_celery_beat',
        'constance',
        'constance.backends.database'
    ]

    LOCAL_APPS = [
        'apps.base',
        'apps.youtube',
        'libs'
    ]

    # Dependent Settings
    INSTALLED_APPS = property(
        lambda self: self.DJANGO_APPS + self.HEALTH_CHECK_APPS + self.THIRD_PARTY_APPS + self.LOCAL_APPS
    )

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'data_center.urls'

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

    WSGI_APPLICATION = 'data_center.wsgi.application'
    ASGI_APPLICATION = "data_center.routing.application"


    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'psqlextra.backend',
            'NAME': os.environ.get("POSTGRESQL_DB_NAME"),
            'USER': os.environ.get("POSTGRESQL_DB_USER"),
            'PASSWORD': os.environ.get("POSTGRESQL_DB_PASSWORD"),
            'HOST': os.environ.get("POSTGRESQL_DB_HOST") or "localhost",
            'PORT': os.environ.get("POSTGRESQL_DB_PORT") or "5432",
        },
    }

    CACHES = {
        'default': {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{os.environ.get('CACHE_LOCATION') or '127.0.0.1:6379/1'}",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "data_center"
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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
    # https://docs.djangoproject.com/en/3.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.0/howto/static-files/
    STATIC_URL = os.environ.get('STATIC_URL', '/api/data_center/static/')
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Third party settings

    # rest framework
    REST_FRAMEWORK = {
        'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
        'DEFAULT_PAGINATION_CLASS': 'apps.base.pagination.CustomLimitOffsetPagination',
        'PAGE_SIZE': 10,
        'DEFAULT_RENDERER_CLASSES': ('djangorestframework_camel_case.render.CamelCaseJSONRenderer',),
        'DEFAULT_PARSER_CLASSES': (
            'djangorestframework_camel_case.parser.CamelCaseFormParser',
            'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
            'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        ),
        'EXCEPTION_HANDLER': 'data_center.apps.base.exception_handler.custom_exception_handler',
        'DEFAULT_AUTHENTICATION_CLASSES': (),
    }

    SWAGGER_SETTINGS = {
        "DEFAULT_PAGINATOR_INSPECTORS": [
            'apps.base.inspectors.LimitOffsetPaginatorInspectorClass',
        ]
    }

    # Sentry Settings
    # Add settings when you want to insert sentry settings
    RAVEN_CONFIG = {}

    # Custom Settings

    TESTING = False

    # Internal Platform secrets
    PLATFORMS_SECRETS = {}

    # YouTube API Key
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
