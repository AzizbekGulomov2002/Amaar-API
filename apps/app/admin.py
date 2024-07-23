from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'address_uz')
    search_fields = ('address_uz',)
    inlines = [OrderItemInline]

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order__address_uz', 'product__name_uz')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name_uz',)

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uz',)
    search_fields = ('name_uz',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('color', 'product')
    search_fields = ('color', 'product__name_uz')
    # Additional configurations as needed


@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')

@admin.register(PolicyAndPrivacy)
class PolicyAndPrivacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')

@admin.register(PublicOffer)
class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')

@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')