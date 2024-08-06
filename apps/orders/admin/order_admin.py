from django.contrib import admin

from apps.orders.models.orders import Order, OrderHistory, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order__address', 'product')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
    search_fields = ('address',)
    inlines = [OrderItemInline]


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['order__id', 'user__username']
