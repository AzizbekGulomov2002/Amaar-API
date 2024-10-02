from django.db import models

from apps.orders.models.orders import Order
from apps.orders.models.products import Product


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        FAILED = 'failed', 'Failed'
        CANCELED = 'canceled', 'Canceled'
        SUCCEEDED = 'succeeded', 'Succeeded'
        EXPIRED = 'expired', 'Expired'
        PENDING = 'pending', 'Pending'

    class TypeOrder(models.TextChoices):
        CASH = 'cash', 'Cash'
        STRIPE = 'stripe', 'Stripe'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    stripe_session_id = models.CharField(max_length=200, null=True, blank=True) #
    created_at = models.DateTimeField(auto_now_add=True) 
    type_order = models.CharField(max_length=20, choices=TypeOrder.choices, default=TypeOrder.STRIPE)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Payments'
