
from datetime import datetime
from typing import Any

from celery import shared_task, chord, group
from django.core.mail import send_mail
from django.db.models import Prefetch

from .models import SubscriptionWeather
from apps.weather.models import City, WeatherData
from apps.weather.serializers import WeatherDataSerializer
from apps.users.models import User

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
    list_of_cities_by_user = {}
    for sub in list_of_subscriptions:
        user, city = sub["user"], sub["city"]
        if user in list_of_cities_by_user:
            list_of_cities_by_user[user].append(city)
        else:
            list_of_cities_by_user[user] = [city]
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
    cities_by_user = create_list_of_cities_by_user(list_of_subscriptions)
    cities_set = {sub["city"] for sub in list_of_subscriptions}
    fetch_weather_tasks = [
        fetch_weather_data.s(city_id) for city_id in cities_set
    ]
    send_mail_with_weather_tasks = [
        send_mail_with_weather_data.s(user_id, city_ids)
        for user_id, city_ids in cities_by_user.items()
    ]
    group(*fetch_weather_tasks)()
    group(*send_mail_with_weather_tasks)()



@shared_task
def fetch_weather_data(city_id) -> None:
    city_instance = City.objects.get(pk=city_id)
    serializer = WeatherDataSerializer(data={"city": city_instance.pk})
    if serializer.is_valid():
        serializer.save()
    else:
        print(
            f"Some problem with {city_instance.name}: {serializer.errors}"
        )


@shared_task
def send_mail_with_weather_data(user_id, city_ids) -> None:
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

