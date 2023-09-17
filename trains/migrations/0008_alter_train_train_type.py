# Generated by Django 4.2.4 on 2023-09-12 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("trains", "0007_alter_traintype_services"),
    ]

    operations = [
        migrations.AlterField(
            model_name="train",
            name="train_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="train",
                to="trains.traintype",
            ),
        ),
    ]