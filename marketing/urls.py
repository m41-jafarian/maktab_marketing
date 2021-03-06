"""marketing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from orders.views import BasketView, InformatinView, pay_amount, PaymentView
from siteview.views import LogInView
from . import settings
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
handler400 = 'siteview.views.error_400'
handler404 = 'siteview.views.error_404'

routers = routers.DefaultRouter()

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'^admin/login/', LogInView.as_view()),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('', include('siteview.urls')),
    path('cart/', BasketView.as_view(), name='cart'),
    path('shipping/', InformatinView.as_view(), name='shipping'),
    path('payment/', PaymentView.as_view(), name='payment'),

    path('api/', include(routers.urls)),
    path('api-auth/', include('rest_framework.urls')),  ## این برای لاگین کردن ای پی آی هست

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
print("urlpaterns ===",urlpatterns)