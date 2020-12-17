from django.contrib.admin.sites import site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from .models import User,Address,Useremail,Shop
from django.utils.translation import ugettext_lazy as _

# Register your models here.

@admin.register(User)
class userAdmin(BaseUserAdmin):
    list_display = ('email','username','first_name','last_name','is_active', 'is_staff', 'is_superuser')
    # list_filter = ('',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar','mobile')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

@admin.register(Address)
class addressAdmin(admin.ModelAdmin):
    list_display = ('user','city','street','allay','zip_code')

@admin.register(Useremail)
class useremailAdmin(admin.ModelAdmin):
    list_display = ('to_user','subject','body')

@admin.register(Shop)
class shopAdmin(admin.ModelAdmin):
    list_display = ('user','name','slug','discreption','image')