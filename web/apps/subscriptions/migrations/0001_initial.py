# Generated by Django 5.0.2 on 2024-02-17 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.SmallIntegerField(choices=[(1, 'One'), (3, 'Three'), (6, 'Six'), (12, 'Twelve')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.city')),
            ],
        ),
    ]
