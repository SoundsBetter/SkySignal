from django.core.management import BaseCommand
from django.db import IntegrityError

from ...models import City
from ...serializers import CitySerializer
from ...services import CityService

CITIES = [
    "Kyiv",
    "London",
    "Paris",
    "Berlin",
    "Rome",
    "Copenhagen",
    "Amsterdam",
    "Stockholm",
    "Warsaw",
    "Vilnius",
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        service = CityService()
        serializers = [
            CitySerializer(data=city_data)
            for city in CITIES
            if (city_data := service.fetch_city_data(name=city))
        ]
        for serializer in serializers:
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(
                    self.style.SUCCESS(
                    f"Successfully created city: {serializer.validated_data['name']}"
                    )
                )
            else:
                self.stdout.write(self.style.ERROR(
                f"Error creating city. Errors: {serializer.errors}"))