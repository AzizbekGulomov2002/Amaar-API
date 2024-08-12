from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.orders import Order
from .views.send_order_to_telegram import send_order_to_telegram_task


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: send_order_to_telegram_task.delay(instance.id, created=True))
