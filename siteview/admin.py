from django.contrib import admin

# Register your models here.
from siteview.models import SlideShow, AdvertisementSide, SiteSetting


@admin.register(SlideShow)
class SlidShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'background', 'action_text', 'action_url')


@admin.register(AdvertisementSide)
class AdvertisementSideAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle','image', 'action_text', 'action_url')


@admin.register(SiteSetting)
class SlidShowAdmin(admin.ModelAdmin):
    list_display = ('section1', 'section2', 'section3', 'section4', 'section5')