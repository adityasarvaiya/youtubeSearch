"""
WSGI config for data_center project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

import dotenv

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_center.settings.prod')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Settings')

from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()