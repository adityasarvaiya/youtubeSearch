import os

from . import common    # pylint: disable=E0401


class Settings(common.Settings):
    DEBUG = False
    ENVIRONMENT_CODE = os.environ.get('ENVIRONMENT_CODE', 'st')

    ALLOWED_HOSTS = '*'