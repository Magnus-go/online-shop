from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from basket.models import Basket, BasketLine
from product.models import Product
from .serializer import BasketLineSerializer, BasketDetailSerializer
from rest_framework import status


class BasketAddView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                basket = Basket.objects.get(user=request.user)
            except:
                basket = Basket.objects.create(user=request.user)

        product_id = request.POST.get('product', None)
        quantity = request.POST.get('quantity', 1)

        try:
            quantity = int(quantity)
        except:
            quantity = 1

        if product_id is not None:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                if BasketLine.objects.filter(product=product).filter(basket=basket).exists():
                    product_line = BasketLine.objects.filter(product=product).filter(basket=basket).first()
                    product_line.basket = basket
                    product_line.quantity += quantity
                    product_line.price = product.price * product_line.quantity
                    product_line.save()
                    srz_data = BasketLineSerializer(instance=product_line)
                    return Response(srz_data.data)

                else:
                    price = product.price
                    product_line = BasketLine.objects.create(
                        basket=basket, product=product, quantity=quantity, price=price * quantity
                    )
                    product_line.save()
                    srz_data = BasketLineSerializer(instance=product_line)
                    return Response(srz_data.data)
        return Response({'error': 'most login'}, status=status.HTTP_401_UNAUTHORIZED)


class ShowUserBasketView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            basket = get_object_or_404(Basket, user=request.user)
            if request.user == basket.user:
                srz_data = BasketDetailSerializer(instance=basket)
                price_list = []
                products_lists = srz_data.data['products_added_to_basket']
                for price in products_lists:
                    prices = price['price']
                    prices = int(prices)
                    price_list.append(prices)
                total_price = sum(price_list)
                serialized_data = srz_data.data
                serialized_data['total_price'] = total_price
                basket.total_price = total_price
                return Response(data=serialized_data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class BasketProductDeleteView(APIView):
    def get(self, request, product_id):
        if request.user.is_authenticated:
            basket = Basket.objects.get(user=request.user)
            if basket.user == request.user:
                try:
                    product = Product.objects.get(id=product_id)
                except:
                    return Response({'error': 'product not found'})

                if BasketLine.objects.filter(basket=basket).filter(product=product).exists():
                    basket_line = BasketLine.objects.filter(product=product).filter(basket=basket).first()
                    basket_line.delete()
                    return Response({'success': 'product deleted successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'something went wrong'})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
