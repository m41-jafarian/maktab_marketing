from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
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
from django.db.models import Min
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
            goods_count = 0
            total = 0
            for basket in basketitems:
                ids.append(basket.shop_product.id)
                goods_count += 1 * basket.count
                total += (basket.shop_product.net_price * basket.count)
            print(ids)
            min_val = ShopProduct.objects.order_by('product_id').values('product_id').annotate(Min('price'))
            print("min_val===================================================================",min_val)
            shop_products = ShopProduct.objects.filter(price__in=min_val.values_list('price__min',flat=True))
            print("shop_products=============================================================",shop_products)
            # min_value = request.GET.get('value')
            # print('----------------------------------- max_value ---------------------------', min_value)
            context['shop_products'] = shop_products
            context['total'] = total
            context['goods_count'] = goods_count
        context['mobile_products'] = ShopProduct.objects.filter(product__category=2)
        context['office_products'] = ShopProduct.objects.filter(product__category=4)[:4]
        context['cloth_products'] = ShopProduct.objects.filter(product__category=Category.objects.get(id=11))[:5]
        context2 = get_all_context(self.request)
        context2.update(context)
        print(context2)
        return context2

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


def get_all_context(request):

    categories = Category.objects.all()
    context= {'category_list': categories, 'products': Product.objects.all()[:5]}
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            context['profile'] = profile
        except:
            pass
    if request.user.is_authenticated:
        basketitems = BasketItems.objects.filter(basket__user=request.user)
        context['basketitems'] = basketitems
        ids = []
        goods_count = 0
        total = 0
        for basket in basketitems:
            ids.append(basket.shop_product.id)
            goods_count += 1 * basket.count
            total += (basket.shop_product.net_price * basket.count)
        print(ids)
        products = Product.objects.all()
        shop_products = ShopProduct.objects.filter(product__in=products)
        print(shop_products)
        context['total'] = total
        context['goods_count'] = goods_count
        context['shop_products'] = shop_products
        context['newer'] = ShopProduct.objects.all().order_by('-created_at')[:10]
    print(context)
    return context
