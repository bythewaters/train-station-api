# Generated by Django 4.2.4 on 2023-09-04 17:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0004_traintype_max_speed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="traintype",
            name="max_speed",
        ),
    ]
