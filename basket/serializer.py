from rest_framework import serializers
from product.serializer import ProductDetailSerializer
from .models import Basket, BasketLine
from product.models import Product


class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ('user',)


class BasketDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    products_added_to_basket = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = '__all__'

    def get_products_added_to_basket(self, obj):
        result = obj.lines.all()
        return BasketLineSerializer(instance=result, many=True).data


class BasketLineSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = BasketLine
        fields = "__all__"
