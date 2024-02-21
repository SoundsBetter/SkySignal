from django.db import models
from django.db.models import UniqueConstraint


class SubscriptionWeather(models.Model):
    class Period(models.IntegerChoices):
        ONE = 1
        THREE = 3
        SIX = 6
        TWELVE = 12


    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    city = models.ForeignKey("weather.City", on_delete=models.CASCADE)
    period = models.SmallIntegerField(choices=Period.choices, default=Period.ONE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "city"], name="unique_user_city")
        ]

    def __str__(self):
        return f'{self.user} - {self.city} - {self.period}'
