# Generated by Django 4.2.4 on 2023-09-06 06:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journies", "0002_alter_journey_arrival_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="journey",
            name="trip_price",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
