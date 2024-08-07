from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from apps.orders.models.orders import Order, OrderHistory, OrderItem


class OrderItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                product = form.cleaned_data['product']
                quantity = form.cleaned_data['quantity']
                if product.quantity < quantity:
                    raise ValidationError(
                        f"Insufficient quantity for product {product.name_uz}. Available: {product.quantity}, Requested: {quantity}")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    formset = OrderItemInlineFormSet
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'type_order', 'order_status', 'payment_status',
        'address', 'latitude', 'longitude', 'comment', 'created_at',)
    search_fields = ('address',)
    readonly_fields = ('payment_status',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order__address', 'product')


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['order__id', 'user__username']
