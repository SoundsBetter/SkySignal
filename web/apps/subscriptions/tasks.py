import json
from time import sleep

import redis
from datetime import datetime
from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Prefetch

from .models import SubscriptionWeather
from apps.weather.models import City, WeatherData
from apps.weather.serializers import WeatherDataSerializer
from apps.users.models import User

redis_client = redis.Redis(host="redis", port=6379, db=0)
pubsub = redis_client.pubsub()

pubsub.subscribe("tasks_channel")


def check_subscription(period: int) -> None:
    now_timestamp = datetime.now().timestamp()
    res_cities = [
        {"city": sub.city.id, "user": sub.user.id}
        for sub in SubscriptionWeather.objects.filter(period=period).all()
    ]
    redis_client.setex(
        name=f"check_subscriptions_{now_timestamp}",
        time=60,
        value=json.dumps(res_cities),
    )


@shared_task
def check_subscriptions_one() -> None:
    return check_subscription(1)


@shared_task
def check_subscriptions_three() -> None:
    return check_subscription(3)


@shared_task
def check_subscriptions_six() -> None:
    return check_subscription(6)


@shared_task
def check_subscriptions_twelve() -> None:
    return check_subscription(12)


@shared_task
def aggregated_results_hourly() -> None:
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
    redis_client.setex(
        name=f"aggregated_results",
        time=60,
        value=json.dumps(aggregate_results),
    )


def create_list_of_cities_by_user(
    aggregate_results: list[dict[str, int]]
) -> dict[int, list[int]]:
    list_of_cities_by_user = {}
    for sub in aggregate_results:
        user, city = sub["user"], sub["city"]
        if user in list_of_cities_by_user:
            list_of_cities_by_user[user].append(city)
        else:
            list_of_cities_by_user[user] = [city]
    return list_of_cities_by_user



@shared_task
def fetch_weather_data() -> None:
    sleep(0.3)
    aggregated_results_json = redis_client.get("aggregated_results")
    aggregated_results = json.loads(aggregated_results_json.decode("utf-8"))
    cities_set = {data["city"] for data in aggregated_results}
    with transaction.atomic():
        for city_id in cities_set:
            city_instance = City.objects.get(pk=city_id)
            serializer = WeatherDataSerializer(data={"city": city_instance.pk})
            if serializer.is_valid():
                serializer.save()
            else:
                print(
                    f"Some problem with {city_instance.name}: {serializer.errors}"
                )


@shared_task
def send_mail_with_weather_data() -> None:
    sleep(2)
    aggregated_results_json = redis_client.get("aggregated_results")
    aggregated_results = json.loads(aggregated_results_json.decode("utf-8"))
    list_of_cities_by_user = create_list_of_cities_by_user(aggregated_results)

    for user_id, city_ids in list_of_cities_by_user.items():
        weather_data_for_user = []
        user = User.objects.get(pk=user_id)
        cities = City.objects.filter(pk__in=city_ids).prefetch_related(
            Prefetch(
                "weather_data_set",
                 queryset=WeatherData.objects.order_by("-datetime"),
                to_attr="latest_weather_data",
            )
        )
        for city in cities:
            if city.latest_weather_data:
                weather_data_for_user.append(
                    city.latest_weather_data[0].data
                )

        send_mail(
            subject=f"Weather data for {user}",
            message=f"{weather_data_for_user}",
            from_email=f"fake@gmail.com",
            recipient_list=[user.email],
        )

