from os.path import dirname, abspath, join, exists
import os


class LoggerSettingsMixin:
    """
    Log Settings Mixin
    """

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue'
            }
        },
        'handlers': {
            'null': {
                'level': 'INFO',
                'class': 'logging.NullHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
                'formatter': 'verbose'
            },
            'error_console': {              # To track the traceback
                'level': 'ERROR',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'INFO',
                'propagate': True,
            },
            'django': {
                'handlers': ['console', 'error_console'],
                'level': 'INFO',
                'propagate': False,
            },
            'apps': {
                'handlers': ['console', 'error_console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            # Catch All Logger -- Captures any other logging
            '': {
                'handlers': ['console', 'error_console'],
                'level': 'INFO',
                'propagate': False,
            }
        }
    }
