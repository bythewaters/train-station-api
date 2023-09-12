# Generated by Django 4.2.4 on 2023-09-08 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_alter_ticket_order"),
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="ticket",
        ),
        migrations.AddField(
            model_name="payment",
            name="order",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.order",
            ),
            preserve_default=False,
        ),
    ]
