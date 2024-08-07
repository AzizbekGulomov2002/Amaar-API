from rest_framework import serializers

from apps.orders.models.payment import Payment


class GeneratePaymentLinkSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
