from celery import shared_task

from .models import SubscriptionWeather

@shared_task
def check_subscriptions_one():
    data = SubscriptionWeather.objects.filter(period=1).all()
    return [sub.id for sub in data]

@shared_task
def check_subscriptions_three():
    data = SubscriptionWeather.objects.filter(period=3).all()
    return [sub.id for sub in data]

@shared_task
def check_subscriptions_six():
    data = SubscriptionWeather.objects.filter(period=6).all()
    return [sub.id for sub in data]

@shared_task
def check_subscriptions_twelve():
    data = SubscriptionWeather.objects.filter(period=12).all()
    return [sub.id for sub in data]