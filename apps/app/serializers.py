from rest_framework import serializers
from apps.app.models import Banner, Category, Product, OrderItem, Order






class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'description_uz', 'price', 'category', 'images']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'image', 'products']


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'image']
#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     if hasattr(self.context.get('view'), 'action'):
#     #         if self.context.get('view').action == 'retrieve':
#     #             products_query = instance.product_set.all()
#     #             products_data = ProductSerializer(products_query, many=True).data
#     #             return {
#     #                 **representation,
#     #                 'products_count': len(products_data),
#     #                 'products': products_data
#     #             }
#     #     return representation

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title_uz', 'description_uz', 'image', 'product']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','address_uz', 'latitude_uz', 'longitude_uz', 'comment_uz', 'products']

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