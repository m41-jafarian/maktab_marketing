from django.urls import path
from marketing.urls import routers

from products.api import ProductViewSet, CategoryViewSet, CommentViewSet, ShopProductViewSet
from products.views import ProductView, CategorySingle, create_comment, search_what, favorite_product, createproduct, \
    createshopproduct, CategoryCreateView, BrandCreateView, ShopCreateView, ProductMetaCreateView, ProductCreateView, \
    ShopProductCreateView, commentlike, Reviews

routers.register(r'products',ProductViewSet)
routers.register(r'categories',CategoryViewSet)
routers.register(r'comments',CommentViewSet)
routers.register(r'shopproducts',ShopProductViewSet)


urlpatterns = [
    path('<int:pk>/', ProductView.as_view(), name='product_id'),
    path('category/<slug:slug>/', CategorySingle.as_view(), name='category_slug'),
    path('sort/', Reviews.as_view(), name='sort'),
    path('createcomment/', create_comment, name='create_comment'),
    path('search/', search_what, name='search_what'),
    path('favorite_add/', favorite_product, name='favorite_add'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('createshopproduct/', ShopProductCreateView.as_view(), name='createshopproduct'),
    path('createCategory/', CategoryCreateView.as_view(), name='createCategory'),
    path('createBrand/', BrandCreateView.as_view(), name='createBrand'),
    path('createShop/', ShopCreateView.as_view(), name='createShop'),
    path('createProductMeta/', ProductMetaCreateView.as_view(), name='createProductMeta'),
    path('commentlike/', commentlike, name='comment_like'),
]
