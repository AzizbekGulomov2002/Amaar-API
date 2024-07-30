from django.db import models
from apps.users.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name_uz or self.name_ru or self.name_en

    class Meta:
        ordering = ['name_uz', 'name_ru', 'name_en']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)

    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)

    # price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.FloatField()
    stripe_price_id = models.CharField(max_length=15)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # images = models.JSONField(default=list, null=True, blank=True)

    best_deals = models.BooleanField(default=False)

    def __str__(self):
        return self.name_uz or self.name_ru or self.name_en

    class Meta:
        ordering = ['name_uz', 'name_ru', 'name_en']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'





class ProductImage(models.Model):
    product = models.ForeignKey("Product", related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        return f"Image for {self.product}"


class Banner(models.Model):
    color = models.CharField(max_length=255)

    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)

    image = models.ImageField(upload_to='banners/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Banner {self.id} - {self.color}"

    class Meta:
        ordering = ['color']
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'


class Order(models.Model):

    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),  # waiting
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)  # Update related_name here
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

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
        verbose_name = 'Order History'
        verbose_name_plural = 'Order Histories'
        ordering = ['-date']


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'






class DeliveryInfo(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50] 

class PolicyAndPrivacy(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50] 

class PublicOffer(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50] 

class ReturnPolicy(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50] 