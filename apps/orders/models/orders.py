from django.core.exceptions import ValidationError
from django.db import models

from apps.orders.models.products import Product
from apps.users.models import User


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        DELIVERED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'
        SUCCESS = 'success', 'Success'

    class TypeOrder(models.TextChoices):
        CASH = 'cash', 'Cash'
        STRIPE = 'stripe', 'Stripe'

    class PaymentStatus(models.TextChoices):
        FAILED = 'failed', 'Failed'
        CANCELED = 'canceled', 'Canceled'
        SUCCEEDED = 'succeeded', 'Succeeded'
        EXPIRED = 'expired', 'Expired'
        PENDING = 'pending', 'Pending'

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    type_order = models.CharField(max_length=20, choices=TypeOrder.choices, default=TypeOrder.STRIPE)
    order_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Orders'

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.products.all())

    def save(self, *args, **kwargs):
        from apps.orders.models.payment import Payment

        if self.type_order == 'cash':
            if self.order_status == 'delivered':
                self.payment_status = 'succeeded'
                Payment.objects.filter(order=self).update(status='succeeded')
            elif self.order_status == 'canceled':
                self.payment_status = 'canceled'
                Payment.objects.filter(order=self).update(status='canceled')
                for item in self.products.all():
                    item.restore_product_quantity()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def clean(self):
        if self.product.quantity < self.quantity:
            raise ValidationError(
                f"Insufficient quantity for product {self.product.name_uz}. Available: {self.product.quantity}, Requested: {self.quantity}")

    def save(self, *args, **kwargs):
        if self.pk is None and self.order.type_order == 'cash':
            self.product.quantity -= self.quantity
            if self.product.quantity < 0:
                raise ValidationError(f"Insufficient quantity for product {self.product.name_uz}.")
        self.product.save()
        super().save(*args, **kwargs)

    def restore_product_quantity(self):
        if self.order.type_order == 'cash':
            self.product.quantity += self.quantity
            self.product.save()

    def __str__(self):
        return f"{self.quantity} of {self.product.name_uz}"

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Order Items'


class OrderHistory(models.Model):
    user = models.ForeignKey(User, related_name='order_histories', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Order Histories'
        ordering = ['-date']
