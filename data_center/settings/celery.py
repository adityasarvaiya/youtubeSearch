import os

from celery.schedules import crontab


class CelerySettingsMixin:

    CELERY_TIMEZONE = 'UTC'

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or "redis://localhost:6379"

    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND") or CELERY_BROKER_URL

    DEFAULT_CELERY_QUEUE = "youtube_default"

    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

    CELERY_BEAT_SCHEDULE = {}
