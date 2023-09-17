from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from notifications.email_notifications import send_email_notifications
from orders.models import Ticket, Order
from payment.models import Payment
from payment.payment_session import create_payment_session
from users.models import User


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
        session_url, session_id, all_tickets_price = create_payment_session(
            order
        )
        for ticket_data in tickets_data:
            ticket = Ticket.objects.create(order=order, **ticket_data)
            send_email_notifications(
                subject="info@cd.cz",
                message="Dear Customer,\n"
                "Thank you for using our services.\n "
                "Please find attached the purchased travel document(s).\n"
                f"Item: {ticket.journey.__str__()}\n"
                f"Order No. {order.id}\n"
                f"Transaction Code: {session_id[5:10].upper()}\n"
                f"Cargo: {ticket_data['cargo']}\n"
                f"Seat: {ticket_data['seat']}\n"
                f"Date of issue: {timezone.now().date()}\n"
                f"Date of validity: {ticket.journey.departure_time.date()}\n"
                f"Price: {ticket.journey.trip_price} USD",
                recipient=(User.objects.get(id=order.user_id).email,),
            )
        Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            order=order,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=all_tickets_price,
        )
        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_time")
