from django.contrib.admin.sites import site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from .models import User,Address,Useremail,Shop,Profile
from django.utils.translation import ugettext_lazy as _

# Register your models here.

@admin.register(User)
class userAdmin(BaseUserAdmin):
    list_display = ('email','is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
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

@admin.register(Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','address','phone_number','mobile_number')