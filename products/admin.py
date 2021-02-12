from django.contrib.admin.sites import site
from django.contrib import admin
from .models import Product, Brand, Category, GalleryImage, Comment, ShopProduct, ProductMeta, CommentLike
from django.utils.translation import ugettext_lazy as _


# Register your models here.

class ProductMetaInline(admin.TabularInline):
    model = ProductMeta

class GalleryImagesInline(admin.TabularInline):
    model = GalleryImage

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ('brand', 'id', 'name', 'slug', 'detail', 'category', 'image')
    inlines =(ProductMetaInline,GalleryImagesInline,CommentInline,)


@admin.register(Brand)
class brandAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'category','detail', 'image')

class BrandInline(admin.TabularInline):
    model = Brand

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'detail', 'parent', 'image')
    inlines =(BrandInline,)


# @admin.register(GalleryImage)
# class galleryImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'id', 'image')

@admin.register(Comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'product', 'text', 'rate')

@admin.register(ShopProduct)
class shopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'id', 'product', 'price', 'quantity','discount','created_at')

@admin.register(ProductMeta)
class shopProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'label', 'value')

@admin.register(CommentLike)
class commentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'id', 'condition')