import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "aggregated": {
        "task": "apps.subscriptions.tasks.aggregated_results_hourly",
        "schedule": settings.MIN_PERIOD
    },
    "one": {
        "task": "apps.subscriptions.tasks.check_subscriptions_one",
        "schedule": settings.MIN_PERIOD,
    },
    "three": {
        "task": "apps.subscriptions.tasks.check_subscriptions_three",
        "schedule": settings.MIN_PERIOD * 3,
    },
    "six": {
        "task": "apps.subscriptions.tasks.check_subscriptions_six",
        "schedule": settings.MIN_PERIOD * 6,
    },
    "twelve": {
        "task": "apps.subscriptions.tasks.check_subscriptions_twelve",
        "schedule": settings.MIN_PERIOD * 12,
    },
    "fetch_weather_data": {
        "task": "apps.subscriptions.tasks.fetch_weather_data",
        "schedule": settings.MIN_PERIOD
    }
}
