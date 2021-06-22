import random
import string

from . import development   #pylint: disable=E0401


class Settings(development.Settings):

    TESTING = True      # Implies test settings/environment

    # Generate a secret key for a single test run
    SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

    development.Settings.CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        "KEY_PREFIX": "data_center_test"
    }

    CONSTANCE_DBS = ['default']
    CONSTANCE_BACKEND = 'constance.backends.memory.MemoryBackend'

    CELERY_TASK_ALWAYS_EAGER = True  # Only to be used for testing purposes

    PLATFORMS_SECRETS = {
        'TestV2Token': {
            'SECRET_KEY':'abc',
            'PLATFORM': 'test'
        }
    }