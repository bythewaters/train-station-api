# Generated by Django 4.2.4 on 2023-09-06 07:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("journies", "0003_journey_trip_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journey",
            name="trip_price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
