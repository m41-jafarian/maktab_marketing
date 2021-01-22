from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

# Create your views here.
from accounts.forms import LoginForm
from accounts.models import Profile
from orders.models import BasketItems
from products.models import Category, Product, ShopProduct
from siteview.forms import UserRegistrationForm
from siteview.models import SlideShow
from django.contrib.auth import get_user_model
User = get_user_model()

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = SlideShow.objects.all()[:3]
        context['category_list'] = Category.objects.all()
        context['products'] = Product.objects.all()[:5]
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                context['profile'] = profile
            except:
                pass
        if self.request.user.is_authenticated:
            basketitems = BasketItems.objects.filter(basket__user=self.request.user)
            context['basketitems']=basketitems
            ids = []
            goods_count=0
            total = 0
            for basket in basketitems:
                ids.append(basket.shop_product.id)
                goods_count += 1 * basket.count
                total += (basket.shop_product.price * basket.count)
            print(ids)
            shop_products = ShopProduct.objects.filter(id__in=ids)
            print(shop_products)
            context['total'] = total
            context['goods_count'] = goods_count
        print(context)
        return context

class LogInView(LoginView):
    template_name = 'base/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        elif self.request.user.is_superuser:
            return reverse("home_index")
        else:
            return reverse("home_index")


class LogOutView(LogoutView):
    pass


class RegisterCreateUser(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'base/register.html'
    success_url = reverse_lazy('login')