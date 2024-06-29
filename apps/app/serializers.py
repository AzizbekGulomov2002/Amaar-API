from rest_framework import serializers
from apps.app.models import Banner, Category, Product, OrderItem, Order


class CategorySerializer(serializers.ModelSerializer):
    # image = serializers.CharField(max_length=50000)
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'images']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'description', 'image', 'product']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','address', 'latitude', 'longitude', 'comment', 'products']

    def create(self, validated_data):
        items_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class DashboardSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_users = serializers.IntegerField()
    users_for_this_month = serializers.IntegerField()
    users_for_this_week = serializers.IntegerField()
    users_for_today = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_banner = serializers.IntegerField()
    orders_by_day = serializers.ListField(child=serializers.DictField())
    top_products = serializers.ListField(child=serializers.DictField())
    top_users = serializers.ListField(child=serializers.DictField())
    top_categories = serializers.ListField(child=serializers.DictField())