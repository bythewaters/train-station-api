from rest_framework import serializers

from orders.serializer import OrderSerializer
from payment.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "order",
            "session_url",
            "session_id",
            "money_to_pay",
        ]


class PaymentDetailSerializer(PaymentListSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "order",
            "session_url",
            "session_id",
            "money_to_pay",
        ]
