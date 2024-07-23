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

    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.JSONField(default=list)

    def __str__(self):
        return self.name_uz or self.name_ru or self.name_en

    class Meta:
        ordering = ['name_uz', 'name_ru', 'name_en']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


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
    address_uz = models.CharField(max_length=255, null=True, blank=True)
    address_ru = models.CharField(max_length=255, null=True, blank=True)
    address_en = models.CharField(max_length=255, null=True, blank=True)

    latitude_uz = models.FloatField(null=True, blank=True)
    latitude_ru = models.FloatField(null=True, blank=True)
    latitude_en = models.FloatField(null=True, blank=True)

    longitude_uz = models.FloatField(null=True, blank=True)
    longitude_ru = models.FloatField(null=True, blank=True)
    longitude_en = models.FloatField(null=True, blank=True)

    comment_uz = models.TextField(null=True, blank=True)
    comment_ru = models.TextField(null=True, blank=True)
    comment_en = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'


class DeliveryInfo(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50]  # Return first 50 characters of name_uz

class PolicyAndPrivacy(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50]  # Return first 50 characters of name_uz

class PublicOffer(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50]  # Return first 50 characters of name_uz

class ReturnPolicy(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    def __str__(self):
        return self.name_uz[:50]  # Return first 50 characters of name_uz