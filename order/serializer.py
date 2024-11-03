from rest_framework import serializers
from .models import Order, OrderItem


class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    orders_product = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_orders_product(self, obj):
        result = obj.items.all()
        return OrdersSerializer(instance=result, many=True).data


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'price', 'quantity')