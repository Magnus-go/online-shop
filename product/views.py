from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category, Subcategory, Comment
from .serializer import (ProductSerializer,
                         CategorySerializer,
                         SubCategorySerializer,
                         ProductDetailSerializer,
                         CommentListSerializer,)
from rest_framework import status


class ProductView(APIView):
    """
    return all existing products or specific category when a slug is provided
    """

    def get(self, request, category_slug=None):
        products = Product.objects.all()
        set_data = ProductSerializer(instance=products, many=True)
        if category_slug:
            products = Product.objects.filter(slug=category_slug)
            ser_data = ProductSerializer(instance=products, many=True)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(set_data.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """
    return a specific product by id of that product
    """

    def setup(self, request, *args, **kwargs):
        self.product_instence = get_object_or_404(Product, pk=kwargs['product_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.product_instence
        ser_data = ProductDetailSerializer(instance=product)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class Categories(APIView):

    def get(self, request):
        categories = Category.objects.all()
        srz_data = CategorySerializer(categories, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class SubCategories(APIView):

    def get(self, request):
        sub_categories = Subcategory.objects.all()
        srz_data = SubCategorySerializer(sub_categories, many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)


class CommentListView(APIView):

    def get(self, request, comment_id=None):
        if not comment_id:
            comments = Comment.objects.all()
            srz_data = CommentListSerializer(instance=comments, many=True)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        else:
            comment = Comment.objects.get(id=comment_id)
            srz_data = CommentListSerializer(instance=comment)
            return Response(srz_data.data, status=status.HTTP_200_OK)


class CommentSendView(APIView):

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        srz_data = CommentListSerializer(data=request.POST)
        if srz_data.is_valid():
            srz_data.save(user=request.user, product=product, available=True)
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
