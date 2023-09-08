import datetime
from typing import Union, Tuple
from unicodedata import decimal

import stripe
from rest_framework.response import Response
from rest_framework.reverse import reverse

from orders.models import Order
from train_station_api import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_session(
    order: Order,
) -> Union[Tuple[str, str, decimal], Response]:
    all_tickets_price = 0
    for ticket in order.tickets.all():
        all_tickets_price += ticket.journey.trip_price
    success_url = reverse("payment:success")
    cancel_url = reverse("payment:cancel")
    payment_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(all_tickets_price * 100),
                    "product_data": {
                        "name": "Train trip",
                        "description": "Thank you for using CESKE DRAHY",
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        metadata={"order_id": order.id},
        success_url=settings.PAYMENT_SUCCESS_URL
        + success_url
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.PAYMENT_FAILED_URL
        + cancel_url
        + "?session_id={CHECKOUT_SESSION_ID}",
    )
    return payment_session.url, payment_session.id, all_tickets_price
