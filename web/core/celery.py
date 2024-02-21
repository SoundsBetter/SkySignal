import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "one": {
        "task": "apps.subscriptions.tasks.check_subscriptions_one",
        "schedule": 2.0,
    },
    "three": {
        "task": "apps.subscriptions.tasks.check_subscriptions_three",
        "schedule": 6.0,
    },
    "six": {
        "task": "apps.subscriptions.tasks.check_subscriptions_six",
        "schedule": 12.0,
    },
    "twelve": {
        "task": "apps.subscriptions.tasks.check_subscriptions_twelve",
        "schedule": 24.0,
    }
}
