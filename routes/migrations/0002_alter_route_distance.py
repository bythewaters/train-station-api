# Generated by Django 4.2.4 on 2023-09-04 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("routes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="route",
            name="distance",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
