from django.contrib.admin.sites import site
from django.contrib import admin
from .models import Product, Brand, Category, GalleryImage, Comment, ShopProduct, ProductMeta, CommentLike, \
    CategoryMeta, CategoryMetaValue, Favorite
from django.utils.translation import ugettext_lazy as _

# Register your models here.

class ProductMetaInline(admin.TabularInline):
    model = ProductMeta

class GalleryImagesInline(admin.TabularInline):
    model = GalleryImage

class CommentInline(admin.TabularInline):
    model = Comment

from django.utils.html import format_html


@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    # fields = ('image_tag',)
    list_display = ('brand', 'id', 'name', 'slug', 'detail', 'category', 'image_tag',)
    readonly_fields = ('image_tag',)
    search_fields = ('slug','name')
    List_Filter = ('brand','category')
    inlines =(ProductMetaInline,GalleryImagesInline,CommentInline,)

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))

@admin.register(Brand)
class brandAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'category','detail', 'image_tag')
    search_fields  = ('slug','name')
    List_Filter = ('category',)

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))

class BrandInline(admin.TabularInline):
    model = Brand

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'detail', 'parent', 'image_tag')
    search_fields  = ('slug','name')
    List_Filter = ('parent',)
    inlines =(BrandInline,)

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))

# @admin.register(GalleryImage)
# class galleryImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'id', 'image')

@admin.register(Comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'product', 'text', 'rate')

@admin.register(ShopProduct)
class shopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'id', 'product', 'price', 'quantity','discount','created_at')
    search_fields  = ('product','shop')
    List_Filter = ('shop',)

@admin.register(ProductMeta)
class shopProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'label', 'value')


class categoryValueInline(admin.TabularInline):
    model = CategoryMetaValue

@admin.register(CategoryMeta)
class categoryMetaAdmin(admin.ModelAdmin):
    list_display = ('category', 'id', 'label')
    inlines = (categoryValueInline,)


@admin.register(CommentLike)
class commentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'id', 'condition')
    search_fields  = ('user','comment')
    List_Filter = ('condition',)
    def make_like(modelAdmin,request,queryset):
        queryset.update(condition=True)
    make_like.short_description = "like selected"


    def make_dislike(modelAdmin,request,queryset):
        queryset.update(condition=False)
    make_dislike.short_description = "dislike selected"


@admin.register(Favorite)
class commentAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop_product', 'id', 'favorite')

    def make_favorite(modelAdmin,request,queryset):
        queryset.update(favorite=True)
    make_favorite.short_description = "like selected"

    def make_disfavorite(modelAdmin,request,queryset):
        queryset.update(favorite=False)
    make_disfavorite.short_description = "dislike selected"