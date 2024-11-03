from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create_order'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
]
