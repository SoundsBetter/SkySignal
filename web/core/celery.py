import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "aggregate": {
        "task": "apps.subscriptions.tasks.aggregate_results_hourly",
        "schedule": 3.0
    },
    "one": {
        "task": "apps.subscriptions.tasks.check_subscriptions_one",
        "schedule": 3.0,
    },
    "three": {
        "task": "apps.subscriptions.tasks.check_subscriptions_three",
        "schedule": 9.0,
    },
    "six": {
        "task": "apps.subscriptions.tasks.check_subscriptions_six",
        "schedule": 18.0,
    },
    "twelve": {
        "task": "apps.subscriptions.tasks.check_subscriptions_twelve",
        "schedule": 36.0,
    }
}
