from django.db import models

from apps.orders.models.products import Product
from apps.users.models import User


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'

    class TypeOrder(models.TextChoices):
        CASH = 'cash', 'Cash'
        STRIPE = 'stripe', 'Stripe'

    class PaymentStatus(models.TextChoices):
        FAILED = 'failed', 'Failed'
        INCOMPLETE = 'incomplete', 'Incomplete'
        CANCELED = 'canceled', 'Canceled'
        SUCCEEDED = 'succeeded', 'Succeeded'
        EXPIRED = 'expired', 'Expired'
        PENDING = 'pending', 'Pending'

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    type_order = models.CharField(max_length=20, choices=TypeOrder.choices, default=TypeOrder.STRIPE)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.products.all())

    def update_status(self, order_status, payment_status):
        if order_status in dict(self.Status.choices) and payment_status in dict(self.PaymentStatus.choices):
            self.status = order_status
            self.payment_status = payment_status
            self.save()
        else:
            raise ValueError("Invalid status or payment status")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name_uz}"

    class Meta:
        ordering = ['order']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class OrderHistory(models.Model):
    user = models.ForeignKey(User, related_name='order_histories', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Order Histories'
        ordering = ['-date']
