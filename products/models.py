from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
User= get_user_model()
# Create your models here.
class Product(models.Model):
    brand = models.ForeignKey("Brand", verbose_name=_("Brand"), on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    category = models.ForeignKey("Category", verbose_name=_("Category"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=50)
    image = models.ImageField(_("Image"), upload_to="product/image", height_field=None, width_field=None, max_length=None)
    detail = models.TextField(_("Detail"))


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})

class Brand(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    detail = models.TextField(_("Detail"))
    image = models.ImageField(_("Image"), upload_to="brand/image", height_field=None, width_field=None, max_length=None)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Brand_detail", kwargs={"pk": self.pk})

class GalleryImage(models.Model):
    product = models.ForeignKey("Product", verbose_name=_(
        "Product"),related_name="product_gallery", on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to="product/gallery", height_field=None, width_field=None, max_length=None)

    class Meta:
        verbose_name = _("GalleryImage")
        verbose_name_plural = _("GalleryImages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Galleryimage_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    detail = models.TextField(_("Detail"))
    image = models.ImageField(_("Image"), upload_to="category/image", height_field=None, width_field=None, max_length=None)
    parent = models.ForeignKey("self", verbose_name=_("parent"),related_name='child' ,on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})

class comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_comment", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey("Product", verbose_name=_(
        "Product"),related_name="product_comment", on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(_("Content"))
    rate = models.IntegerField(_("Rate"))

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})




class ShopProduct(models.Model):
    shop = models.ForeignKey("accounts.Shop", verbose_name=_("Shop"), on_delete=models.CASCADE)
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE)
    price = models.IntegerField(_("Price"))
    quantity = models.IntegerField(_("Quantity"))

    class Meta:
        verbose_name = _("ShopProduct")
        verbose_name_plural = _("ShopProducts")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Shopproduct_detail", kwargs={"pk": self.pk})

class ProductMeta(models.Model):
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE)
    label = models.CharField(_("Label"), max_length=50)
    value  = models.CharField(_("Value"), max_length=50)
    
    class Meta:
        verbose_name = _("ProductMeta")
        verbose_name_plural = _("ProductMetaes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ProductMeta_detail", kwargs={"pk": self.pk})

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_like", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Like_detail", kwargs={"pk": self.pk})
