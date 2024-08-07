from django.db import models
from apps.orders.models import Product
from ckeditor.fields import RichTextField

from apps.users.models import User

# Create your models here.

class SpecialOffer(models.Model):
    image = models.ImageField(upload_to='special_offers/')
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='special_offers')

    def __str__(self):
        return self.title_en

class Company(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title

class News(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    desc_uz = RichTextField()
    desc_ru = RichTextField()
    desc_en = RichTextField()
    image = models.ImageField(upload_to='news/')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='news')

    def __str__(self):
        return self.title_en


class Recall(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.client.username}"