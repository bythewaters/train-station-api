# Generated by Django 4.2.4 on 2023-09-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0006_traintype_max_speed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="traintype",
            name="services",
            field=models.ManyToManyField(
                null=True, related_name="train_type", to="trains.service"
            ),
        ),
    ]
