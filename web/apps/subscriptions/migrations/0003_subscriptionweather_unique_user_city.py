# Generated by Django 5.0.2 on 2024-02-20 11:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_initial'),
        ('weather', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscriptionweather',
            constraint=models.UniqueConstraint(fields=('user', 'city'), name='unique_user_city'),
        ),
    ]