import os

from . import staging


class Settings(staging.Settings):
    ENVIRONMENT_CODE = os.environ.get('ENVIRONMENT_CODE', 'pd')