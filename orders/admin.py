from django.contrib import admin

from orders.models import Order, Ticket

admin.site.register(Order)
admin.site.register(Ticket)
