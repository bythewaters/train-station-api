from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from journies.test.test_journeys_api import create_journey
from orders.models import Order, Ticket
from payment.models import Payment
from payment.payment_session import create_payment_session
from train_station_api import settings
from users.models import User
from unittest.mock import patch, Mock


class CreatePaymentSessionTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test_user@example.com", password="password"
        )
        self.client.force_authenticate(self.user)
        self.order = Order.objects.create(
            user=self.user
        )
        self.tickets = Ticket.objects.create(
            cargo=1,
            seat=2,
            journey=create_journey(),
            order=self.order
        )

    def test_create_payment_session(self):
        mock_session = Mock(
            id="test_session_id",
            url="http://test-session-url.com",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 9.99,
                        "product_data": {
                            "name": self.tickets.journey.train.name,
                            "description": "Ticket price",
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_FAILED_URL,
        )

        with patch(
                "stripe.checkout.Session.create",
                return_value=mock_session
        ):
            session_url, session_id, all_tickets_price = create_payment_session(
                self.order
            )

        payment = Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            order=self.order,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=self.tickets.journey.trip_price,
        )
        self.assertEqual(session_id, "test_session_id")
        self.assertEqual(session_url, "http://test-session-url.com")
        payment.refresh_from_db()
        self.assertEqual(payment.status, "PENDING")
        self.assertEqual(payment.type, "PAYMENT")
        self.assertEqual(payment.order, self.order)
        self.assertEqual(float(payment.money_to_pay), self.tickets.journey.trip_price)
        self.assertEqual(
            settings.PAYMENT_SUCCESS_URL + reverse("payment:success"),
            "http://localhost:8000/api/train-station/payment/success/",
        )
        self.assertEqual(
            settings.PAYMENT_FAILED_URL + reverse("payment:cancel"),
            "http://localhost:8000/api/train-station/payment/cancel/",
        )
