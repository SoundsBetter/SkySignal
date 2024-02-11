from django.db import models


class Subscription(models.Model):
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

    def __str__(self):
        return f'{self.user} - {self.city} - {self.period}'
