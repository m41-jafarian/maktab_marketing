from django.contrib import admin

# Register your models here.
from siteview.models import SlideShow


@admin.register(SlideShow)
class SlidShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'background', 'action_text', 'action_url')
