from collections import defaultdict
from datetime import datetime
from time import sleep
from typing import Any
from celery import shared_task, chord, group, chain
from django.core.mail import send_mail
from django.db.models import Prefetch
from celery.utils.log import get_task_logger

from apps.weather.models import City, WeatherData
from apps.weather.services import WeatherDataService
from apps.subscriptions.models import SubscriptionWeather
from apps.users.models import User

logger = get_task_logger(__name__)


def get_tasks_for_current_time() -> list[Any]:
    tasks = []
    now = datetime.now()

    tasks.append(check_subscriptions.s(1))
    if now.hour % 3 == 0:
        tasks.append(check_subscriptions.s(3))

    if now.hour % 6 == 0:
        tasks.append(check_subscriptions.s(6))

    if now.hour % 12 == 0:
        tasks.append(check_subscriptions.s(12))
    return tasks


def create_list_of_cities_by_user(
    list_of_subscriptions: list[dict[str, int]]
) -> dict[int, list[int]]:
    list_of_cities_by_user = defaultdict(list)
    for sub in list_of_subscriptions:
        user, city = sub["user"], sub["city"]
        list_of_cities_by_user[user].append(city)
    return list_of_cities_by_user


@shared_task
def check_subscriptions(period: int) -> list[dict[str, int]]:
    res_cities = [
        {"city": sub.city.id, "user": sub.user.id}
        for sub in SubscriptionWeather.objects.filter(period=period).all()
    ]
    return res_cities


@shared_task
def get_subscriptions_every_hour():
    tasks = get_tasks_for_current_time()
    callback = process_subscription_results.s()
    chord(tasks)(callback)


@shared_task
def process_subscription_results(result: list[list[dict[str, int]]]):
    list_of_subscriptions = [sub for subs in result for sub in subs]
    cities_set = {sub["city"] for sub in list_of_subscriptions}
    cities_by_user = create_list_of_cities_by_user(list_of_subscriptions)
    fetch_weather_tasks = group(
        fetch_weather_data.s(city_id) for city_id in cities_set
    )
    send_mail_with_weather_tasks = group(
        send_mail_with_weather_data.s(user_id=user_id, city_ids=city_ids)
        for user_id, city_ids in cities_by_user.items()
    )
    chain(
        fetch_weather_tasks,
        send_mail_with_weather_tasks,
    ).apply_async()




@shared_task
def fetch_weather_data(city_id) -> None:
    logger.info(f"Fetching weather data for {city_id}")
    sleep(3)
    city_instance = City.objects.get(pk=city_id)
    data = WeatherDataService().fetch_weather_data(
        lat=city_instance.lat, lon=city_instance.lon
    )
    WeatherData.objects.create(city=city_instance, data=data)


@shared_task
def send_mail_with_weather_data(*args, **kwargs) -> None:
    user_id = kwargs.get('user_id')
    city_ids = kwargs.get('city_ids')
    logger.info(f"Sending {city_ids} weather data for {user_id}")
    sleep(7)
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
            weather_data_for_user.append(city.latest_weather_data[0].data)

    send_mail(
        subject=f"Weather data for {user}",
        message=f"{weather_data_for_user}",
        from_email=f"fake@gmail.com",
        recipient_list=[user.email],
    )
