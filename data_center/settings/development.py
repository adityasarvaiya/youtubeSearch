import os

from . import common    # pylint: disable=E0401


class Settings(common.Settings):

    DEBUG = True
    ENVIRONMENT_CODE = os.environ.get('ENVIRONMENT_CODE', 'dev')
    ALLOWED_HOSTS = ['*']