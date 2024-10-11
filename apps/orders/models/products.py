from django.db import models


class TranslatableModel(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name_uz[:50]

class Category(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    name_ru = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name_en} - {self.name_ru}"

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Categories'

class Product(TranslatableModel):
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE
    )
    
    best_deals = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    show_main_page = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "Product {self.name_ru}"

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/',null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name_uz}"

    
    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = 'Product images'
