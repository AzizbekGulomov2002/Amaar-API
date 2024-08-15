from rest_framework import serializers

from apps.orders.models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'stripe_charge_id', 'amount', 'created_at']
