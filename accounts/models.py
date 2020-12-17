from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    email =  models.EmailField(_("email"), max_length=254,blank=False,unique=True)
    avatar = models.ImageField(_("avatar"), upload_to="user/avatar", height_field=None, width_field=None, max_length=None)
    mobile = models.IntegerField(_("mobile"),blank=True, null=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)
    def get_full_name(self):
        return self.first_name+" "+self.last_name
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_profile", on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
    def __str__(self):
        return self.user
    def get_absolute_url(self):
        return reverse("Profile_detail", kwargs={"pk": self.pk})

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="address_user_profile", on_delete=models.CASCADE)
    city = models.CharField(_("City"), max_length=50)
    street = models.CharField(_("Street"), max_length=50)
    allay = models.CharField(_("Allay"), max_length=50)
    zip_code = models.IntegerField(_("Zip_code"))
    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
    def __str__(self):
        return self.city

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})
class Useremail(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("To_user"), on_delete=models.CASCADE)
    subject = models.CharField(_("Subject"), max_length=50)
    body = models.TextField(_("Body"))
    class Meta:
        verbose_name = _("UserEmail")
        verbose_name_plural = _("UserEmails")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("Email_detail", kwargs={"pk": self.pk})

class Shop(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_shop", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_("Name"), max_length=50)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    discreption = models.TextField(_("Descreption")) 
    image = models.ImageField(_("Image"), upload_to="shop/image", height_field=None, width_field=None, max_length=None)
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("Shop_detail", kwargs={"pk": self.pk})
