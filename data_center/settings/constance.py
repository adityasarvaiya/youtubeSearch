from collections import OrderedDict


class LiveSettingsMixin:
    """
    Contains All Live-settings variable in one place
    """

    # Constance Variables
    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

    CONSTANCE_ADDITIONAL_FIELDS = {
        'json': [
            'django.contrib.postgres.forms.JSONField', {
                'widget': 'django_json_widget.widgets.JSONEditorWidget'
            }
        ],
        'password_field': [
            'django.forms.fields.CharField', {
                'widget': 'django.forms.PasswordInput',
                'widget_kwargs': {"render_value": True}
            }
        ]
    }

    CONSTANCE_CONFIG = {
        'SEARCH_QUERY': (
            'Cricket',
            'Search query on which youtube data to be fetched.'
        ),
        'EPOCHS': (
            3,
            'Number of times youtube search response to be fetched in a particular task execution.'
        ),
        'DEFAULT_LATEST_VIDEO_DATETIME': (
            '2021-06-02T16:42:19Z',
            'This will be used for syncing youtube videos for the very first time.'
        )
    }

    CONSTANCE_CONFIG_FIELDSETS = OrderedDict([
        ("General", ['SEARCH_QUERY', 'EPOCHS', 'DEFAULT_LATEST_VIDEO_DATETIME']),
    ])
