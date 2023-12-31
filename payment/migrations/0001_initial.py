# Generated by Django 4.2.4 on 2023-09-08 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orders", "0002_alter_ticket_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "Pending"), ("PAID", "Paid")],
                        max_length=63,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PAYMENT", "Payment"), ("FINE", "Fine")],
                        max_length=63,
                    ),
                ),
                ("session_url", models.URLField(blank=True, max_length=500, null=True)),
                ("session_id", models.CharField(blank=True, max_length=250, null=True)),
                ("money_to_pay", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orders.ticket"
                    ),
                ),
            ],
        ),
    ]
