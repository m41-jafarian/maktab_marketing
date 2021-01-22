from django.contrib.admin.sites import site
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from .models import User,Address,Useremail,Shop,Profile
from django.utils.translation import ugettext_lazy as _

# Register your models here.

@admin.register(User)
class userAdmin(BaseUserAdmin):
    list_display = ('email','id','is_active', 'is_staff', 'is_superuser')

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


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(userAdmin):
    inlines = (ProfileInline, )
    list_display = ( 'email',  'is_staff','id',)


    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Address)
class addressAdmin(admin.ModelAdmin):
    list_display = ('user','city','street','allay','zip_code','id',)

@admin.register(Useremail)
class useremailAdmin(admin.ModelAdmin):
    list_display = ('to_user','id','subject','body')

@admin.register(Shop)
class shopAdmin(admin.ModelAdmin):
    list_display = ('user','name','id','slug','discreption','image')

@admin.register(Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ('first_name','id','last_name','address','phone_number','mobile_number')