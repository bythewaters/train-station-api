from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import Ticket, Order
from payment.models import Payment
from payment.payment_session import create_payment_session


class TicketSerializer(serializers.ModelSerializer):
    trip_price = serializers.IntegerField(
        source="journey.trip_price", read_only=True
    )

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["cargo"],
            attrs["seat"],
            attrs["journey"].train,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey", "trip_price")


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("cargo", "seat", "journey")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_time")

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(order=order, **ticket_data)

        session_url, session_id, ticket_cost = create_payment_session(order)
        Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            order=order,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=ticket_cost,
        )



class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_time")
