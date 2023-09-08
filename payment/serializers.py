from rest_framework import serializers

from orders.serializer import TicketSerializer
from payment.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "ticket",
            "session_url",
            "session_id",
            "money_to_pay",
        ]


class PaymentDetailSerializer(PaymentListSerializer):
    borrowing = TicketSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "ticket",
            "session_url",
            "session_id",
            "money_to_pay",
        ]
