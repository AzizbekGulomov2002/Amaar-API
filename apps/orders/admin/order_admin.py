from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from apps.orders.models.orders import Order, OrderHistory, OrderItem
from apps.orders.models.payment import Payment


class OrderItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                product = form.cleaned_data['product']
                quantity = form.cleaned_data['quantity']
                if product.quantity < quantity:
                    raise ValidationError(
                        f"Insufficient quantity for product {product.name_uz}. "
                        f"Available: {product.quantity}, Requested: {quantity}"
                    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    formset = OrderItemInlineFormSet
    extra = 1


class OrderAdminForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def save(self, commit=True):
        print(f"Saving Order: {self.instance}")
        order = super().save(commit=False)

        if not order.pk:
            order.save()
            print(f"Order saved with ID: {order.pk}")

        if order.type_order == 'cash':
            if order.order_status == 'pending':
                order.order_status = 'success'
                order.payment_status = 'pending'
            elif order.order_status == 'delivered':
                order.payment_status = 'succeeded'
                Payment.objects.filter(order=order).update(status='succeeded')
            elif order.order_status == 'canceled':
                order.payment_status = 'canceled'
                Payment.objects.filter(order=order).update(status='canceled')
                for item in order.products.all():
                    product = item.product
                    product.quantity += item.quantity
                    product.save()
            else:
                for item in order.products.all():
                    product = item.product
                    product.quantity -= item.quantity
                    product.save()

            for item in order.products.all():
                Payment.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    status=order.payment_status,
                    type_order='cash',
                )

        if commit:
            order.save()
        return order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'type_order', 'order_status', 'payment_status',
        'address', 'latitude', 'longitude', 'comment', 'created_at',)
    search_fields = ('address',)
    readonly_fields = ('payment_status',)
    list_per_page = 10
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
