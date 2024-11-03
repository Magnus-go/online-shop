from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baskets')
    total_price = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    def delete_basket_lines(self, request):
        basket = Basket.objects.get(user=request.user)
        basket_lines = BasketLine.objects.filter(basket=basket)
        basket_lines.delete()


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lines')
    price = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.basket} =>> {self.product} ==> {self.quantity}'
