import json
from datetime import datetime, timedelta

import redis
from celery import shared_task

from apps.weather.serializers import CitySerializer

from .models import SubscriptionWeather

redis_client = redis.Redis(host="redis", port=6379, db=0)
pubsub = redis_client.pubsub()

pubsub.subscribe("tasks_channel")


def check_subscription(period: int):
    res_cities = [
        {"city": sub.city.id, "user": sub.user.id}
        for sub in SubscriptionWeather.objects.filter(period=period).all()
    ]
    redis_client.set(
        f"task_one_{datetime.now().timestamp()}", json.dumps(res_cities)
    )
    return res_cities


@shared_task
def check_subscriptions_one():
    return check_subscription(1)


@shared_task
def check_subscriptions_three():
    return check_subscription(3)


@shared_task
def check_subscriptions_six():
    return check_subscription(6)


@shared_task
def check_subscriptions_twelve():
    return check_subscription(12)


@shared_task
def aggregate_results_hourly():
    now_timestamp = datetime.now().timestamp()
    one_hour_ago = now_timestamp - 3

    aggregate_results = []

    for key in redis_client.keys("task_*"):
        _, task_timestamp = key.decode().rsplit("_", 1)
        task_timestamp = float(task_timestamp)

        if one_hour_ago <= task_timestamp <= now_timestamp:
            result_ids = json.loads(redis_client.get(key))
            aggregate_results.extend(result_ids)
    return aggregate_results
