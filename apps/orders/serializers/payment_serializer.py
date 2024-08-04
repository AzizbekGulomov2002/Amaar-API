from rest_framework import serializers

from apps.orders.models.payment import Payment


class GeneratePaymentLinkSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'stripe_charge_id', 'amount', 'created_at']
