from django.urls import path

from products.views import ProductView, CategorySingle, create_comment

urlpatterns = [
    path('<int:pk>/', ProductView.as_view(), name='product_id'),
    path('category/<slug:slug>/', CategorySingle.as_view(), name='category_id'),
    path('createcomment/', create_comment, name='create_comment'),
]
