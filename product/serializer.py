from rest_framework import serializers
from .models import Product, Category, Subcategory, Comment


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'price', 'category', 'sub_category', 'available', 'created')


class ProductDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_comments(self, obj):
        result = obj.product_comments.filter(available=True)
        return CommentListSerializer(result, many=True).data


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('category_title', 'sub_categories')

    def get_sub_categories(self, obj):
        result = obj.subcategories.all()
        return SubCategorySerializer(instance=result, many=True).data


class SubCategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.StringRelatedField()
    all_related_products = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = '__all__'

    def get_all_related_products(self, obj):
        result = obj.products.all()
        return ProductSerializer(instance=result, many=True).data


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            'user': {'read_only': True},
            'product': {'read_only': True},
        }
