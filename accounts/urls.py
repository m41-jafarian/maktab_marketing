from django.urls import path
from accounts.views import ProfileView, edit_user, edit_profile, update_avatar, edit_address, ShopView, ShopDetailView

urlpatterns = [
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('update/<int:pk>', edit_user, name='account_update'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('update_avatar/', update_avatar, name='update_avatar'),
    path('edit_address/', edit_address, name='edit_address'),
    path('shops/', ShopView.as_view(), name='shop'),
    path('shops/<slug:slug>', ShopDetailView.as_view(), name='shop_slug'),
]