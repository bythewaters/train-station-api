from django.db import models

from orders.models import Ticket


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT"
        FINE = "FINE"

    status = models.CharField(max_length=63, choices=Status.choices)
    type = models.CharField(max_length=63, choices=Type.choices)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    session_url = models.URLField(max_length=500, null=True, blank=True)
    session_id = models.CharField(max_length=250, null=True, blank=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"Payment #{self.id}: "
            f"{self.status} {self.type} for ticket #{self.ticket_id}"
        )
