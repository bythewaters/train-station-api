# Generated by Django 4.2.4 on 2023-09-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0008_alter_train_train_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="traintype",
            name="services",
            field=models.ManyToManyField(
                related_name="train_type", to="trains.service"
            ),
        ),
    ]
