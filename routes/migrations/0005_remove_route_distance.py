# Generated by Django 4.2.4 on 2023-09-10 20:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("routes", "0004_merge_20230906_0636"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="route",
            name="distance",
        ),
    ]
