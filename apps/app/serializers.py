from rest_framework import serializers
from apps.app.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'price', 'category', 'images']

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image', 'products']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'color', 'description_uz', 'description_ru', 'description_en', 'image', 'product']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'address_uz', 'address_ru', 'address_en', 'latitude_uz', 'latitude_ru', 'latitude_en', 'longitude_uz', 'longitude_ru', 'longitude_en', 'comment_uz', 'comment_ru', 'comment_en', 'products']

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



class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = ['id', 'name_uz', 'name_ru', 'name_en']

class DeliveryInfoListSerializer(serializers.ListSerializer):
    child = DeliveryInfoSerializer()
    allow_empty = False

    def create(self, validated_data):
        delivery_infos = [DeliveryInfo(**item) for item in validated_data]
        return DeliveryInfo.objects.bulk_create(delivery_infos)



class PolicyAndPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyAndPrivacy
        fields = ['id', 'name_uz', 'name_ru', 'name_en']

class PolicyAndPrivacyListSerializer(serializers.ListSerializer):
    child = PolicyAndPrivacySerializer()
    allow_empty = False

    def create(self, validated_data):
        policies = [PolicyAndPrivacy(**item) for item in validated_data]
        return PolicyAndPrivacy.objects.bulk_create(policies)

class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ['id', 'name_uz', 'name_ru', 'name_en']

class PublicOfferListSerializer(serializers.ListSerializer):
    child = PublicOfferSerializer()
    allow_empty = False

    def create(self, validated_data):
        offers = [PublicOffer(**item) for item in validated_data]
        return PublicOffer.objects.bulk_create(offers)

class ReturnPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnPolicy
        fields = ['id', 'name_uz', 'name_ru', 'name_en']

class ReturnPolicyListSerializer(serializers.ListSerializer):
    child = ReturnPolicySerializer()
    allow_empty = False

    def create(self, validated_data):
        return_policies = [ReturnPolicy(**item) for item in validated_data]
        return ReturnPolicy.objects.bulk_create(return_policies)

