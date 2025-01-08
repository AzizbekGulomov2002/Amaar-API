from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models.orders import OrderItem, Order, OrderHistory
from apps.orders.models.payment import Payment
from apps.orders.models.products import Product
from apps.orders.serializers.product_serializer import ProductSerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = [
            'id', 'address', 'latitude', 'longitude', 'comment', 'products',
            'user', 'created_at', 'type_order', 'order_status', 'payment_status'
        ]

    def validate_products(self, products):  # noqa
        for product_data in products:
            product = Product.objects.get(id=product_data['product'].id)
            if product.quantity < product_data['quantity']:
                raise ValidationError(f"Insufficient quantity for product {product.name_uz}")
        return products



    def create(self, validated_data):
        products_data = validated_data.pop('products')
        user = validated_data.pop('user')
        order_type = validated_data.get('type_order', Order.TypeOrder.STRIPE)

        # Determine initial status
        if order_type == Order.TypeOrder.STRIPE:
            validated_data['order_status'] = Order.Status.PENDING
            validated_data['payment_status'] = Order.PaymentStatus.PENDING
        else:
            validated_data['order_status'] = Order.Status.SUCCESS
            validated_data['payment_status'] = Order.PaymentStatus.PENDING

        # Create the order
        order = Order.objects.create(user=user, **validated_data)

        # Create order items
        for product_data in products_data:
            OrderItem.objects.create(order=order, **product_data)
            if order_type == Order.TypeOrder.CASH:
                product = product_data['product']
                product.quantity -= product_data['quantity']
                product.save()

        # Handle payments
        if order_type == Order.TypeOrder.CASH:
            Payment.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=product_data['quantity'],
                status=Payment.PaymentStatus.PENDING,
                type_order=Order.TypeOrder.CASH
            )
            return self.to_representation(order)

        payment_link_data = ProductSerializer.generate_payment_link(order.products.all(), self.context['request'])

        for product_data in products_data:
            Payment.objects.create(
                order=order,
                product=product_data['product'],
                price=product_data['product'].price,
                quantity=product_data['quantity'],
                status=Payment.PaymentStatus.PENDING,
                stripe_session_id=payment_link_data['session_id'],
                type_order=Order.TypeOrder.STRIPE,
            )

        # Add payment link to response
        order_data = self.to_representation(order)
        order_data['payment_link'] = payment_link_data['payment_url']

        return order_data
    


    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)
        representation['products'] = [
            {
                'id': item.product.id,
                'name_uz': item.product.name_uz,
                'name_ru': item.product.name_ru,
                'name_en': item.product.name_en,
                'description_uz': item.product.description_uz,
                'description_ru': item.product.description_ru,
                'description_en': item.product.description_en,
                'quantity': item.quantity,
                'price': item.product.price,
                'images': [
                    request.build_absolute_uri(image.image.url)
                    for image in item.product.product_images.all()
                ] if request else []
            } for item in instance.products.all()
        ]

        representation['user'] = {
            'id': instance.user.id,
            'name': instance.user.name,
            'phone_number': instance.user.phone_number
        } if instance.user else None

        representation['order_status'] = instance.order_status
        representation['payment_status'] = instance.payment_status

        return representation


    # def create(self, validated_data):
    #     products_data = validated_data.pop('products')
    #     user = validated_data.pop('user')
    #     order_type = validated_data.get('type_order', Order.TypeOrder.STRIPE)

    #     if order_type == Order.TypeOrder.STRIPE:
    #         order_status = Order.Status.PENDING
    #         payment_status = Order.PaymentStatus.PENDING
    #     else:
    #         order_status = Order.Status.SUCCESS
    #         payment_status = Order.PaymentStatus.PENDING

    #     order = Order.objects.create(user=user, order_status=order_status, payment_status=payment_status,
    #                                  **validated_data)

    #     for product_data in products_data:
    #         OrderItem.objects.create(order=order, **product_data)
    #         if order_type == Order.TypeOrder.CASH:
    #             product = product_data['product']
    #             product.quantity -= product_data['quantity']
    #             product.save()

    #     if order_type == Order.TypeOrder.CASH:
    #         Payment.objects.create(
    #             order=order,
    #             product=product,
    #             price=product.price,
    #             quantity=product_data['quantity'],
    #             status=Payment.PaymentStatus.PENDING,
    #             type_order=Order.TypeOrder.CASH
    #         )
    #         return self.to_representation(order)

    #     payment_link_data = ProductSerializer.generate_payment_link(order.products.all(), self.context['request'])

    #     for product_data in products_data:
    #         Payment.objects.create(
    #             order=order,
    #             product=product_data['product'],
    #             price=product_data['product'].price,
    #             quantity=product_data['quantity'],
    #             status=Payment.PaymentStatus.PENDING,
    #             stripe_session_id=payment_link_data['session_id'],
    #             type_order=Order.TypeOrder.STRIPE,
    #         )

    #     order_data = self.to_representation(order)
    #     order_data['payment_link'] = payment_link_data['payment_url']

    #     return order_data




    



class OrderHistoryIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['id', 'order', 'user', 'date', 'status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['order'] = OrderSerializer(instance.order).data
        return representation

class OrderHistoryBaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['id', 'order', 'user', 'date', 'status']

    def create(self, validated_data):
        order_history = super().create(validated_data)
        order = order_history.order
        order.status = order_history.status
        order.save()
        return order_history

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        order = instance.order
        order.status = instance.status
        order.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation