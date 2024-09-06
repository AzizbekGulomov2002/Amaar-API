from ckeditor.fields import RichTextField
from django.db import models

from apps.orders.models.products import Product


class TranslatableModel(models.Model):
    name_uz = RichTextField()
    name_ru = RichTextField()
    name_en = RichTextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name_uz[:50]


class Banner(models.Model):
    # color = models.CharField(max_length=255)  
    title_uz = models.TextField(null=True, blank=True)
    title_ru = models.TextField(null=True, blank=True)
    title_en = models.TextField(null=True, blank=True)
    
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Banner {self.id}"



class DeliveryInfo(TranslatableModel):
    def __str__(self):
        return self.name_uz[:25]


class PolicyAndPrivacy(TranslatableModel):
    def __str__(self):
        return self.name_uz[:25]


class PublicOffer(TranslatableModel):
    def __str__(self):
        return self.name_uz[:25]


class ReturnPolicy(TranslatableModel):
    def __str__(self):
        return self.name_uz[:25]
