from django.urls import path
from accounts.views import ProfileView, edit_user

urlpatterns = [
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('update/<int:pk>', edit_user, name='account_update'),
]