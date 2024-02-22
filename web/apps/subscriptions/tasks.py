import json
from time import sleep

import redis
from datetime import datetime
from celery import shared_task

from .models import SubscriptionWeather
from apps.weather.services import WeatherService
from apps.weather.models import City

redis_client = redis.Redis(host="redis", port=6379, db=0)
pubsub = redis_client.pubsub()

pubsub.subscribe("tasks_channel")


def check_subscription(period: int):
    now_timestamp = datetime.now().timestamp()
    res_cities = [
        {"city": sub.city.id, "user": sub.user.id}
        for sub in SubscriptionWeather.objects.filter(period=period).all()
    ]
    redis_client.setex(
        name=f"check_subscriptions_{now_timestamp}",
        time=3600,
        value=json.dumps(res_cities),
    )


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
def aggregated_results_hourly():
    sleep(0.1)
    now_timestamp = datetime.now().timestamp()
    one_hour_ago = now_timestamp - 3

    aggregate_results = []

    for key in redis_client.keys("check_subscriptions_*"):
        _, task_timestamp = key.decode().rsplit("_", 1)
        task_timestamp = float(task_timestamp)

        if one_hour_ago <= task_timestamp <= now_timestamp:
            result_ids = json.loads(redis_client.get(key))
            aggregate_results.extend(result_ids)
    redis_client.set(
        name=f"aggregated_results",
        value=json.dumps(aggregate_results),
    )


@shared_task
def fetch_weather_data():
    service = WeatherService()
    sleep(0.3)
    aggregated_results_json = redis_client.get("aggregated_results")
    aggregated_results = json.loads(aggregated_results_json.decode('utf-8'))
    cities_set = {data["city"] for data in aggregated_results}
    cites = [City.objects.get(pk=city) for city in cities_set]
    for city in cites:
        print(city)
    weather_data = [
        service.fetch_weather_data(lat=city.lat, lon=city.lon)
        for city in cites
    ]
    print(weather_data)


