from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.BasketAddView.as_view(), name='add_to_basket'),
    path('', views.ShowUserBasketView.as_view(), name='show_user_basket'),
    path('delete/<int:product_id>/', views.BasketProductDeleteView.as_view(), name='product_basket_delete'),
]

