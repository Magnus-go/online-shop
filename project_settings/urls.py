from django.contrib import admin
from django.urls import path, include


# project's Main URL Conf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('users/', include('user.urls')),
    path('products/', include('product.urls')),
    path('basket/', include('basket.urls')),
    path('order/', include('order.urls')),
    path('profile/', include('user_profile.urls')),
]
