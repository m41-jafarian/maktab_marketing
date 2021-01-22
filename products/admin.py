from django.contrib.admin.sites import site
from django.contrib import admin
from .models import Product,Brand,Category,GalleryImage,Comment,ShopProduct,ProductMeta
from django.utils.translation import ugettext_lazy as _


# Register your models here.
@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ('brand', 'id', 'name', 'slug', 'detail', 'category', 'image')

@admin.register(Brand)
class brandAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'detail', 'image')

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'detail', 'parent', 'image')

@admin.register(GalleryImage)
class galleryImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'image')

@admin.register(Comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'product', 'text', 'rate')

@admin.register(ShopProduct)
class shopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'id', 'product', 'price', 'quantity')

@admin.register(ProductMeta)
class shopProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'label', 'value')
