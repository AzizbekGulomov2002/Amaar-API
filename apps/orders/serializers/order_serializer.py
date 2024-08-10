from rest_framework import serializers

from apps.orders.models.orders import OrderItem, Order, OrderHistory
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
        fields = ['id', 'address', 'latitude', 'longitude', 'comment', 'products', 'user', 'created_at', 'status']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        user = validated_data.pop('user')
        order = Order.objects.create(user=user, **validated_data)
        for product_data in products_data:
            OrderItem.objects.create(order=order, **product_data)
        return order

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
                'amount': item.quantity,
                'price': item.product.price,
                'images': [
                    request.build_absolute_uri(image.image.url)
                    for image in item.product.images.all()
                ] if request else []
            } for item in instance.products.all()
        ]

        representation['user'] = {
            'id': instance.user.id,
            'name': instance.user.name,
            'phone_number': instance.user.phone_number
        } if instance.user else None

        return representation


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
