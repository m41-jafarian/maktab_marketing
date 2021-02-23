from django.urls import path
from marketing.urls import routers

from products.api import ProductViewSet, CategoryViewSet, CommentViewSet, ShopProductViewSet
from products.views import ProductView, CategorySingle, create_comment, search_what, favorite_product, createproduct, \
    createshopproduct, CategoryCreateView, BrandCreateView, ShopCreateView, ProductMetaCreateView, ProductCreateView, \
    ShopProductCreateView, commentlike, Reviews, CategotyMetaCreateView, EditCategory, EditView, EditBrand, EditProfile, \
    EditProduct, EditShop, EditShopProduct, CategoryMetaVAlueView

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
    path('createCategoryMeta/', CategotyMetaCreateView.as_view(), name='createCategoryMeta'),
    path('createCategoryMetaValue/', CategoryMetaVAlueView.as_view(), name='createCategoryMetaValue'),
    path('commentlike/', commentlike, name='comment_like'),
    path('updateCategory/<slug:slug>/', EditCategory.as_view(), name='updateCategory'),
    path('updateBrand/<slug:slug>/', EditBrand.as_view(), name='updateBrand'),
    path('updateProfile/<int:pk>/', EditProfile.as_view(), name='updateProfile'),
    path('updateProduct/<int:pk>/', EditProduct.as_view(), name='updateProduct'),
    path('updateShop/<int:pk>/', EditShop.as_view(), name='updateShop'),
    path('updateShopProduct/<int:pk>/', EditShopProduct.as_view(), name='updateShopProduct'),

    path('update/', EditView.as_view(), name='edit'),

]
