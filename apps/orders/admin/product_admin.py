from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.orders.models.products import Product, ProductImage, Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    can_delete = True
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # change_form_template = "admin/orders/product/change_form.html"
    inlines = [ProductImageInline]
    list_display = ('id', 'name_uz', 'price', 'quantity', 'category', 'best_deals', 'view_button')
    search_fields = ('name_uz', 'name_ru', 'name_en')
    ordering = ('-created_at',)
    add_form_template = 'admin/orders/add_btn.html'
    change_form_template = add_form_template

    @admin.display(description='View Product')
    def view_button(self, obj):
        url = reverse('admin:orders_product_change', args=[obj.pk])
        return format_html(
            '<a class="view-button" href="#" onclick="viewProduct({id}); return false;">'
            '<i class="fas fa-eye"></i></a>',
            id=obj.pk
        )
