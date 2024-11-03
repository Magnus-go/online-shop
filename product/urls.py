from django.urls import path
from . import views


urlpatterns = [
    path('comments/', views.CommentListView.as_view(), name='comments_list'),
    path('comments/detail/<int:comment_id>/', views.CommentListView.as_view(), name='comments_detail'),
    path('comments/<int:product_id>/', views.CommentSendView.as_view(), name='comments_send'),
    path('categories/', views.Categories.as_view(), name='categories_list'),
    path('sub_categories/', views.SubCategories.as_view(), name='sub_categories_list'),
    path('', views.ProductView.as_view(), name='product_view'),
    path('<slug:category_slug>/', views.ProductView.as_view(), name='product_view'),
    path('detail/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
]
