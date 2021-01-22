from django.http import HttpResponse, request
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import json
from accounts.models import Shop, Profile
from orders.models import Basket, BasketItems, OrderItems, Order
from products.models import Product, ShopProduct, Category
from django.contrib.auth import get_user_model

User = get_user_model()


# basketitems = BasketItems.objects.create(basket_id=1,shop_product_id=1)
# print(basketitems)
# shop_products = {}
# for basket in basketitems:
#     shop_products.update({basket: {"shop_name": basket.shop_product.shop.name,
#                                    "product_name": basket.shop_product.product.name,
#                                    "product_url": basket.shop_product.product.image,
#                                    "price": basket.shop_product.price}})


class BasketView(ListView):
    model = BasketItems
    template_name = 'components/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['shops'] = Shop.objects.all()
        context['category_list'] = Category.objects.all()
        # shop_products = {}
        # for basket in context['basketitems_list']:
        #     shop_products.update({basket: {"shop_name": basket.shop_product.shop.name,
        #                                    "product_name": basket.shop_product.product.name,
        #                                    "product_url": basket.shop_product.product.image,
        #                                    "price": basket.shop_product.price}})
        if self.request.user.is_authenticated:
            basketitems = BasketItems.objects.filter(basket__user=self.request.user)
            context['basketitem_list']=basketitems
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
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                context['profile'] = profile
            except:
                pass
        return context



@csrf_exempt
def add_product_cart(request):
    data = json.loads(request.body)
    user = request.user
    shp_id = data['shp_id']
    print(shp_id)
    print(user.id)
    print(user)
    try:
        print("------------------------------------exist basket")
        basket = Basket.objects.get(user=user)
    except Basket.DoesNotExist:
        print("------------------------------------created basket")
        basket = Basket.objects.create(user=user)
    try:
        try:
            basketitems = BasketItems.objects.get(basket_id=basket.id, shop_product_id=shp_id)
            print("basketitems ------in to try avaliyast ----->",basketitems)
            if basketitems:
                print("injam miyad?")
                basketitems.count=basketitems.count+1
                basketitems.save()
                print("basketitems.count==",basketitems.count)
                response = {"mok": "mok"}
                print(response)
                return HttpResponse(json.dumps(response), status='201')

            else:
                basketitems = BasketItems.objects.create(basket_id=basket.id, shop_product_id=shp_id)
                print(basketitems)
                response = {"ok": "ok"}
                print(response)
                return HttpResponse(json.dumps(response), status='201')
        except:
            basketitems = BasketItems.objects.create(basket_id=basket.id, shop_product_id=shp_id)
            print(basketitems)
            response = {"ok": "ok"}
            print(response)
            return HttpResponse(json.dumps(response), status='201')
    except :
            print("erradeh")
            response = ["error"]
            return HttpResponse(json.dumps(response), status='400')


@csrf_exempt
def delete_basket_items(request):
    data = json.loads(request.body)
    user = request.user
    BasketItems.objects.filter(basket__user=request.user).delete()
    response = {"ok": "ok"}
    return HttpResponse(json.dumps(response), status='201')

@csrf_exempt
def delete_basket_item(request):
    data = json.loads(request.body)
    print("data======",data)
    shp_id = data['shopproduct_id']
    print("shopproduct_id==",shp_id)
    user = request.user
    try:
        print("------------------------------------exist basket")
        basket = Basket.objects.get(user=user)
    except Basket.DoesNotExist:
        print("------------------------------------created basket")
        basket = Basket.objects.create(user=user)
    try:
        basketitems = BasketItems.objects.get(basket_id=basket.id, shop_product_id=shp_id)
        print("basketitems ------in to try avaliyast ----->",basketitems)
        if basketitems.count>1:
            print("injam miyad?")
            basketitems.count=basketitems.count-1
            basketitems.save()
            print("basketitems.count==",basketitems.count)
            response = {"mok": "mok"}
            print(response)
            return HttpResponse(json.dumps(response), status='201')
        else:
            del_item = BasketItems.objects.filter(basket__user=request.user).filter(shop_product_id=shp_id).first()
            del_item.delete()
            basket_items = BasketItems.objects.all()
            print(basket_items)
            response = {"ok":"ok"}
            print("response===========================",response)
            return HttpResponse(json.dumps(response), status='201')
    except:
        print("error delete item")
        return HttpResponse('bad request', status=404)


class OrderItemsView(ListView):
    model = OrderItems
    template_name = "components/shipping.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        basketitems = BasketItems.objects.filter(basket__user=self.request.user)
        try:
            order = Order.objects.get(user=self.request.user)
        except Order.DoesNotExist:
            order = Order.objects.create(user=self.request.user)
        total=0
        goods_count = 0
        OrderItems.objects.filter(order=order).delete()
        for item in basketitems:
            orderItems = OrderItems.objects.create(order=order,shop_product=item.shop_product,price=item.shop_product.price,
                                                   count=item.count)
            total += item.shop_product.price * item.count
            goods_count += 1 * item.count
            orderItems.save()
        context['orderitems'] = OrderItems.objects.filter(order=order)
        context['total'] = total
        context['goods_count'] = goods_count
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                context['profile'] = profile
            except:
                pass
        return context
