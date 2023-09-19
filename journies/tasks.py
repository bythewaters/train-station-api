from django.db import transaction
from django.utils import timezone
from celery import shared_task
from journies.models import Journey


@shared_task(bind=True)
def check_valid_trip(self):
    try:
        with transaction.atomic():
            today = timezone.now()
            Journey.objects.filter(departure_time__lte=today).delete()
    except Exception as e:
        self.retry(exc=e, countdown=60 * 5, max_retries=5)
