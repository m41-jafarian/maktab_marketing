from django.urls import path

from orders.views import delete_basket_items, add_product_cart, delete_basket_item

urlpatterns = [
    path('clear/', delete_basket_items, name='clear_cart'),
    path('add_product/', add_product_cart, name='add_product'),
    path('del_item/', delete_basket_item, name='del_item'),
]