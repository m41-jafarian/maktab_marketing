from django.urls import path

from .views import HomeView, LogInView, LogOutView, RegisterCreateUser, AboutUs

urlpatterns = [
    path('', HomeView.as_view(), name='home_index'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('register/', RegisterCreateUser.as_view(), name='register'),
    path('about_us/', AboutUs.as_view(), name='aboutus'),
]