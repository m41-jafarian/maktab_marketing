from unicodedata import category

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, ListView

from accounts.models import Shop, Profile
from orders.models import BasketItems
from products.forms import CommentForm
from products.models import Category, Product, ShopProduct, GalleryImage,Comment


class ProductView(DetailView):
    model = Product
    template_name = 'components/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['category_list'] = Category.objects.all()
        context['products'] = Product.objects.all()[:5]
        context['shops'] = Shop.objects.filter(shop__product=product)
        context['gallery'] = GalleryImage.objects.filter(product=product)
        # context['shops'] = ShopProduct.objects.filter(product=product)
        context["comments"] = product.comments.all()
        comments = product.comments.all()
        profiles = Profile.objects.all()
        context['profiles'] = profiles
        for comment in comments:
            print(Profile.objects.filter(user=comment.user))
        shops = ShopProduct.objects.filter(product=product)
        context['shops_product'] = ShopProduct.objects.filter(product=product)
        context['form'] = CommentForm()
        print(shops)
        min_prise=9999999999
        for shop in shops:
            if shop.price<min_prise :
                min_shop = shop
                min_prise = shop.price
                shp_id = shop.id
        if min_shop is not None:
            context['min_shop'] = min_shop.shop.name
            context['min_prise'] = min_shop.price
            context['shp_id'] = shp_id
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                context['profile'] = profile
            except:
                pass
        if self.request.user.is_authenticated:
            basketitems = BasketItems.objects.filter(basket__user=self.request.user)
            context['basketitems'] = basketitems
            ids = []
            total = 0
            for basket in basketitems:
                ids.append(basket.shop_product.id)
                total += basket.shop_product.price
            print(ids)
            shop_products = ShopProduct.objects.filter(id__in=ids)
            print(shop_products)
            context['total'] = total
        print(context)
        return context



class CategorySingle(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'components/category.html'

    def get_queryset(self):
        self.slug = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user=self.request.user)

        return context

@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        print("user", user, "datatext", data['text'], "rate", data['rate'], "productid", data['product_id'])
        comment = Comment.objects.create(user=user, product_id=data['product_id'], text=data['text'], rate=data['rate'])
        response = {"like_count": 0,
                    "dislike_count": 0, "text": comment.text, "f_name": user.email,  "comment_id": comment.id}
        print(response)
        return HttpResponse(json.dumps(response), status='201')
    except:
        response = ["error"]
        print((response))
        return HttpResponse(json.dumps(response), status='400')
