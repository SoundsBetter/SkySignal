from django.core.management import BaseCommand
from django.db import IntegrityError

from apps.subscriptions.models import SubscriptionWeather

PERIODS = [1, 3, 6, 12]
USERS = range(1, 6)
CITIES = range(1, 11)
COUNT = 20

class Command(BaseCommand):
    def handle(self, *args, **options):
        for n in range(COUNT):
            try:
                SubscriptionWeather.objects.create(
                    user_id=USERS[n // 4],
                    city_id=CITIES[n % len(CITIES)],
                    period=PERIODS[n % len(PERIODS)],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Subscription created"
                    )
                )
            except IntegrityError as e:
                self.stdout.write(
                    self.style.ERROR(
                        e
                    )
                )

