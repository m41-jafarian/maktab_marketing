from unicodedata import category
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json
# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from accounts.models import Shop, Profile
from orders.models import BasketItems
from products.forms import CommentForm, ProductCreateForm, ShopProductCreateForm, CategoryCreateForm, BrandCreateForm, \
    ShopCreateForm, ProductMetaCreateForm
from products.models import Category, Product, ShopProduct, GalleryImage, Comment, Brand, ProductMeta, Favorite, \
    CommentLike, CategoryMeta, CategoryMetaValue
from django.contrib.auth import get_user_model

from siteview.views import get_all_context

User = get_user_model()


class ProductView(DetailView):
    model = Product
    template_name = 'components/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['shops'] = Shop.objects.filter(shop__product=product)
        context['gallery'] = GalleryImage.objects.filter(product=product)
        context["comments"] = product.comments.all()
        comments = product.comments.all()
        comment_ids = []
        total_rate = 0
        for comment in comments:
            comment_ids.append(comment.user.id)
            total_rate += comment.rate
        print("===================  comments  =========================",comments)
        commentlikes = CommentLike.objects.filter(comment__in=comments)
        print("===================  commentlikes  =========================",commentlikes)
        context['commentlikes'] = commentlikes
        if comments.count() > 0:
            average_rate = total_rate / comments.count()
            context["average_rate"] = average_rate
        print(comment_ids)
        profiles = Profile.objects.filter(user_id__in=comment_ids)
        context['profiles'] = profiles
        context['form'] = CommentForm()
        shops = ShopProduct.objects.filter(product=product)
        context['shops_product'] = ShopProduct.objects.filter(product=product)
        min_price = 9999999999
        for shop in shops:
            net_price = shop.net_price
            if net_price < min_price:
                min_shop = shop
                min_price = net_price
                shp_id = shop.id
                if self.request.user.is_authenticated:
                    try:
                        favorite = Favorite.objects.get(user=self.request.user, shop_product=min_shop)
                    except Favorite.DoesNotExist:
                        favorite = Favorite.objects.create(user=self.request.user, shop_product=min_shop,
                                                           favorite=False)
                else:
                    favorite = ""
        if min_shop is not None:
            context['min_shop'] = min_shop
            context['min_price'] = min_price
            context['discount'] = min_shop.discount
            context['price'] = min_shop.price
            context['shp_id'] = shp_id
            if favorite != "":
                context['favorite'] = favorite.favorite
        categorymeta = CategoryMeta.objects.filter(category=product.category)
        # categoryvalues_id = categorymeta.values_list('category__categorymeta__label', flat=True).distinct()
        categoryvalues = CategoryMetaValue.objects.filter(label__in=categorymeta)
        # for catmeta in categorymeta:
        #     print(catmeta.label.count())
        print("========================  categorymeta  ======================",categorymeta)
        print("========================  categoryvalues  ======================",categoryvalues)
        context['categorymeta'] = categorymeta
        context['categoryvalues'] = categoryvalues
        productmeta = ProductMeta.objects.filter(product=product)
        context['productmeta'] = productmeta
        context2 = get_all_context(self.request)
        context2.update(context)

        print(context2)
        return context2

# @csrf_exempt
# def reviews(request):
#         data = request.body
#         print(data)
#         products = ShopProduct.objects.all.order_by(data)
#         print(products)
#         # response = {"ok":"ok"}
#         # return HttpResponse(response, status='201')
#         context = {
#             'products': products
#         }
#         return render(request, 'components/category.html', context)

class Reviews(ListView):
    model = ShopProduct
    context_object_name = 'products'
    paginate_by = 6
    template_name = "components/category.html"
    queryset = ShopProduct.objects.all().order_by('price')

    def get_queryset(self):
        ordering = self.request.GET.get('sort', None)
        # validate ordering here
        print(ordering)
        queryset = ShopProduct.objects.all().order_by(ordering)
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        context['shops'] = Shop.objects.all()
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user=self.request.user)
        context['min_val'] = 0
        context['max_val'] = 300000
        context2 = get_all_context(self.request)
        context2.update(context)
        return context2


class CategorySingle(ListView):
    model = Product
    paginate_by = 6
    context_object_name = 'products'
    template_name = 'components/category.html'

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            order = self.request.GET.get['orderItem']
            print(order)


    def get_queryset(self):
        # self.slug = get_object_or_404(Category, slug=self.kwargs['slug'])
        cat = get_object_or_404(Category, slug=self.kwargs['slug'])
        print('0000000000000000000000000000000000000  cat  000000000000000000000000000000 ', cat, cat.child.count(),
              cat.child.all())
        if cat.child.count() == 0:
            print('cat child == 0')
            queryset = ShopProduct.objects.filter(product__category=cat)
        else:
            for ch in cat.child.all():
                print(ch.slug)
            queryset = ShopProduct.objects.filter(product__category__in=cat.child.all())
        # return ShopProduct.objects.filter(Q(product__category=self.slug) | Q(product__category__child__exact=self.slug))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        print("tttttttttttttttttttttttttt  kwargs slug  ttttttttttttttttttttttttttttt", self.kwargs['slug'])
        cat = self.kwargs['slug']
        cate = Category.objects.get(slug=cat)
        context['brands'] = Brand.objects.filter(category=cate)
        if cate.child.count() > 0:
            context['sub_categories'] = Category.objects.filter(parent=cate)
        context['shops'] = Shop.objects.all()
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user=self.request.user)
        context['min_val'] = 0
        context['max_val'] = 300000

        context2 = get_all_context(self.request)
        context2.update(context)
        return context2

    # def call_view(self, request, **kwargs):
    #     max_value = request.GET.get('max_value')
    #     print('----------------------------------- max_value ---------------------------',max_value)
    #     context = super().get_context_data(**kwargs)
    #     ccc = ShopProduct.objects.filter(price__gte=5000000,price__lte=20000000)
    #     context['products'] = ccc
    #     return context

@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        print("user", user, "datatext", data['text'], "rate", data['rate'], "productid", data['product_id'])
        comment = Comment.objects.create(user=user, product_id=data['product_id'], text=data['text'], rate=data['rate'])
        CommentLike.objects.create(
            user=user, condition=None, comment=comment)
        profile = Profile.objects.get(user=user)
        if profile.first_name:
            f_name = profile.first_name + " " + profile.last_name
        else:
            f_name = user.email

        created_at = comment.created_at.strftime("%d . %b . %Y . %H:%M")
        response = {"like_count": 0,
                    "dislike_count": 0, "text": comment.text,"rate": data['rate'],"created_at":created_at,"f_name": f_name, "comment_id": comment.id}
        print(response)
        return HttpResponse(json.dumps(response), status='201')
    except:
        response = ["error"]
        print((response))
        return HttpResponse(json.dumps(response), status='400')

@csrf_exempt
def commentlike(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.get(id=data['comment_id'])
    except Comment.DosNotExist:
        return HttpResponse('bad request', status=404)
    try:
        comment_like = CommentLike.objects.get(user=user, comment=comment)
        if comment_like.condition == False and data['condition'] == False or comment_like.condition == True and data['condition'] == True:
            comment_like.condition = None
        else:
            comment_like.condition = data['condition']
        comment_like.save()
        condition = comment_like.condition
    except:
        CommentLike.objects.create(
            user=user, condition=data['condition'], comment=comment)
        condition = data['condition']
    response = {"like_count": comment.like_count,
                "dislike_count": comment.dislike_count, "commentID": data['comment_id'],"condition":condition}
    return HttpResponse(json.dumps(response), status='201')


@csrf_exempt
def search_what(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    users = User.objects.all()
    brands = Brand.objects.all()
    shops = Shop.objects.all()
    context = {
        "products": products,
        "categories": categories,
        "brands": brands,
        "shops": shops,
    }
    if request.method == 'GET':
        search_what = request.GET.get('search_box', None)
        search_brand = request.GET.getlist('brands', None)
        search_shop = request.GET.getlist('shops', None)
        print("search_brand=======", search_brand)
        # search_category = Category.objects.filter(name__icontains=search_what)
        result = ""
        if search_what:
            search_product = ShopProduct.objects.filter(Q(product__name__icontains=search_what) | Q(
                product__brand__name__icontains=search_what) | Q(product__category__name__icontains=search_what))
        else:
            search_product = ShopProduct.objects.all()
        if search_brand:
            search_product = ShopProduct.objects.filter(Q(product__brand__slug__in=search_brand))
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', search_brand)
            # for serch in search_brand:
            #     search_product = ShopProduct.objects.filter(Q(product__brand__slug__icontains=serch))
            #     result = list(chain(result, search_product))
            # search_product = result
        if search_shop:
            search_product = ShopProduct.objects.filter(Q(shop__slug__in=search_shop))
            # for serch in search_shop:
            #     search_product = ShopProduct.objects.filter(Q(shop__slug__icontains=serch))
            #     result = list(chain(result,search_product))
            # search_product = result
        if search_shop and search_brand:
            result = ""
            # for serch1 in search_brand:
            #     for serch2 in search_shop:
            search_product = ShopProduct.objects.filter(
                Q(product__brand__slug__in=search_brand) & Q(shop__slug__in=search_shop))
            # result = list(chain(result, search_product))
            # search_product = result

        context = {
            "search_what": search_what,
            "products": search_product,
            "categories": categories,
            "brands": brands,
            "shops": shops,
            "category_list": categories
        }
        context2 = get_all_context(request)
        context2.update(context)
    return render(request, 'components/category.html', context2)


@csrf_exempt
def favorite_product(request):
    data = json.loads(request.body)
    user = request.user
    favorite_condition = data['favorite']
    try:
        shop_product = ShopProduct.objects.get(id=data['shop_product_id'])
    except ShopProduct.DosNotExist:
        return HttpResponse('bad request', status=404)
    try:
        favorite = Favorite.objects.get(user=user, shop_product=shop_product)
        if favorite.favorite == True and data['favorite'] == True:
            favorite.favorite = False
        else:
            favorite.favorite = data['favorite']
        favorite.save()
    except:
        Favorite.objects.create(
            user=user, favorite=data['favorite'], shop_product=shop_product)
    # response = {"like_count": comment.like_count,
    #             "dislike_count": comment.dislike_count, "commentID": data['comment_id']}
    if favorite.favorite == True:
        favore = 1
    else:
        favore = 0
    response = {"favor": favore, "shop_product_id": shop_product.id}
    return HttpResponse(json.dumps(response), status='201')


class ProductCreateView(CreateView):
# class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    # permission_required = ('products.add_product',)
    template_name = 'components/create.html'
    success_url = reverse_lazy('create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(self.request)
        context2.update(context)
        return context2


class ShopProductCreateView(CreateView):
    model = ShopProduct
    form_class = ShopProductCreateForm
    template_name = 'components/create.html'
    success_url = reverse_lazy('create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(self.request)
        context2.update(context)
        return context2


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'components/create.html'
    success_url = reverse_lazy('create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(self.request)
        context2.update(context)
        return context2


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandCreateForm
    template_name = 'components/create.html'
    success_url = reverse_lazy('create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(self.request)
        context2.update(context)
        return context2


class ShopCreateView(CreateView):
    model = Shop
    form_class = ShopCreateForm
    template_name = 'components/create.html'
    success_url = reverse_lazy('create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(self.request)
        context2.update(context)
        return context2


class ProductMetaCreateView(CreateView):
    model = ProductMeta
    form_class = ProductMetaCreateForm
    template_name = 'components/create.html'
    success_url = reverse_lazy('create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context2 = get_all_context(self.request)
        context2.update(context)
        return context2





@login_required
def createproduct(request):
    form = ProductCreateForm()
    user = request.GET.get('user', None)
    category = request.GET.get('category', None)
    products = Product.objects.all()
    categories = Category.objects.all()
    users = User.objects.all()
    context = {
        "form": form,
        "posts": products,
        "categories": categories,
        "users": users,
    }
    if request.method == 'POST':
        print("----------------------------------post")
        form = ProductCreateForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            image = form.cleaned_data.get("image")
            brand = form.cleaned_data.get("brand")
            slug = form.cleaned_data.get("slug")
            category = form.cleaned_data.get("category")
            detail = form.cleaned_data.get("detail")
            product = Product.objects.create(
                name=name,
                image=image,
                slug=slug,
                detail=detail,
                brand=brand,
                category=category
            )
            product.save()
            print("--------------------------------------------post save", product)
            return render(request, 'home.html', context)

        else:
            context['form'] = form
            return render(request, 'components/create.html', context)
    else:
        print("----------------------------------Get")
        return render(request, 'components/create.html', context)


@login_required
def createshopproduct(request):
    context = get_all_context(request)
    form = ShopProductCreateForm()
    user = request.GET.get('user', None)
    category = request.GET.get('category', None)
    products = Product.objects.all()
    categories = Category.objects.all()
    users = User.objects.all()
    context['form'] = form
    if request.method == 'POST':
        print("----------------------------------post")
        form = ShopProductCreateForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            shop = form.cleaned_data.get("shop")
            product = form.cleaned_data.get("product")
            price = form.cleaned_data.get("price")
            quantity = form.cleaned_data.get("quantity")
            discount = form.cleaned_data.get("discount")
            shopproduct = ShopProduct.objects.create(
                shop=shop,
                product=product,
                price=price,
                discount=discount,
                quantity=quantity,
            )
            shopproduct.save()
            print("--------------------------------------------post save", shopproduct)
            return render(request, 'home.html', context)

        else:
            context['form'] = form
            return render(request, 'components/createshopproduct.html', context)
    else:
        print("----------------------------------Get")
        return render(request, 'components/createshopproduct.html', context)
