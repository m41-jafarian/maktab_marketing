from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

# Create your views here.
from accounts.forms import LoginForm
from accounts.models import Profile, Shop
from orders.models import BasketItems
from products.models import Category, Product, ShopProduct, Brand, Favorite
from siteview.forms import UserRegistrationForm
from siteview.models import SlideShow, AdvertisementSide, SiteSetting
from django.db.models import Min
from django.template import RequestContext
from django.contrib.auth import get_user_model
User = get_user_model()

class HomeView(TemplateView):
    template_name = 'home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slides'] = SlideShow.objects.all()[:4]
        context['category_list'] = Category.objects.all()
        context['products'] = Product.objects.all()[:5]
        context['advertisement'] = AdvertisementSide.objects.filter().first()
        context['shop_products'] = ShopProduct.objects.all()[:12]
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
        sitesetting = SiteSetting.objects.get(id=1)
        if sitesetting.section1 != 0:
            context['section1'] = Category.objects.get(id=sitesetting.section1)
            context['section1_products'] = ShopProduct.objects.filter(product__category=sitesetting.section1)[:4]
        if sitesetting.section2 != 0:
            context['section2'] = Category.objects.get(id=sitesetting.section2)
            context['section2_products'] = ShopProduct.objects.filter(product__category=sitesetting.section2)[:4]
        if sitesetting.section3 != 0:
            context['section3'] = Category.objects.get(id=sitesetting.section3)
            context['section3_products'] = ShopProduct.objects.filter(product__category=sitesetting.section3)[:4]
        if sitesetting.section4 != 0:
            context['section4'] = Category.objects.get(id=sitesetting.section4)
            context['section4_products'] = ShopProduct.objects.filter(product__category=sitesetting.section4)[:4]
        if sitesetting.section5 != 0:
            context['section5'] = Category.objects.get(id=sitesetting.section5)
            context['section5_products'] = ShopProduct.objects.filter(product__category=sitesetting.section5)[:4]
        favorite = Favorite.objects.order_by('-favorite').filter(favorite=True)[:10]
        shopprdct_ids = favorite.values_list('shop_product__product',flat=True)
        favorite_product = ShopProduct.objects.filter(id__in=shopprdct_ids)
        context['favorite_products'] = favorite_product
        context['newer'] = ShopProduct.objects.order_by('-created_at').all()[:10]
        context2 = get_all_context(self.request)
        context2.update(context)
        # print(context2)
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
        context['brand_list'] = Brand.objects.all()
        context['shop_list'] = Shop.objects.all()
        context['product_list'] = Product.objects.all()
    print(context)
    return context


class AboutUs(TemplateView):
    template_name = 'components/about_us.html'


def error_400(request, exception):
    return render(request, '400.html')

def error_404(request, exception):
    return render(request, '404.html')