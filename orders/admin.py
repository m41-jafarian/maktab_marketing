from django.contrib.admin.sites import site
from django.contrib import admin
from .models import Payment,Basket,BasketItems,Order,OrderItems
from django.utils.translation import ugettext_lazy as _
# Register your models here.

@admin.register(Payment)
class paymentAdmin(admin.ModelAdmin):
    list_display = ('id','order','user','amount')

@admin.register(Basket)
class basketAdmin(admin.ModelAdmin):
    list_display = ('id','user')

@admin.register(BasketItems)
class basketItemsAdmin(admin.ModelAdmin):
    list_display = ('id','basket','shop_product')

@admin.register(Order)
class orderAdmin(admin.ModelAdmin):
    list_display = ('id','user','create_at','update_at','description')

@admin.register(OrderItems)
class orderItemsAdmin(admin.ModelAdmin):
    list_display = ('id','order','shop_product','count','price')