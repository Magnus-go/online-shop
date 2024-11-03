from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.generics import get_object_or_404
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from basket.models import Basket, BasketLine
from order.models import Order, OrderItem
from order.serializer import OrderDetailSerializer
import requests


class OrderCreateView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            basket = get_object_or_404(Basket, user=request.user)
            basket_profiles = BasketLine.objects.filter(basket=basket)
            order = Order.objects.create(user=request.user)
            for item in basket_profiles:
                OrderItem.objects.create(order=order, product=item.product, price=item.price, quantity=item.quantity)
            basket.delete_basket_lines(request)
            total_price = order.get_total_price()
            return Response({'message': f'your order cost is {total_price}'})


class OrderDetailView(APIView):
    def get(self, reqeust, order_id):
        if reqeust.user.is_authenticated:
            order = get_object_or_404(Order, id=order_id, user=reqeust.user)
            srz_data = OrderDetailSerializer(instance=order)
            return Response(srz_data.data)


MERCHANT = '6f1c037a-55377d-4f155-86b6-87a1001f0483'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify/'


class OrderPayView(APIView):

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
