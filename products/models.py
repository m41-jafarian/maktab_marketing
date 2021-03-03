from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
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
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='brand_category')

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
    title = models.CharField(_("Title"),max_length=50,null=True,blank=True)

    class Meta:
        verbose_name = _("GalleryImage")
        verbose_name_plural = _("GalleryImages")

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("Galleryimage_detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=128)
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


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="author", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey("Product", verbose_name=_(
        "Product"),related_name="comments", on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(_("Content"))
    rate = models.IntegerField(_("Rate"), null=True, blank=True)
    created_at = models.DateTimeField(_('Created_at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated_at'),auto_now=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})

    @property
    def like_count(self):
        q=CommentLike.objects.filter(comment=self)
        q=q.filter(condition=True)
        return q.count()

    @property
    def dislike_count(self):
        q=CommentLike.objects.filter(comment=self,condition=False)
        return q.count()



class ShopProduct(models.Model):
    shop = models.ForeignKey("accounts.Shop",related_name="shop", verbose_name=_("Shop"), on_delete=models.CASCADE)
    product = models.ForeignKey("Product", verbose_name=_("Product"),related_name="product", on_delete=models.CASCADE)
    price = models.IntegerField(_("Price"))
    quantity = models.IntegerField(_("Quantity"))
    discount = models.IntegerField(_("discount"), default=0)
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True,db_index=True)
    updated_at = models.DateTimeField(_('updated_at'),auto_now=True)

    class Meta:
        verbose_name = _("ShopProduct")
        verbose_name_plural = _("ShopProducts")

    def __str__(self):
        return self.product.name

    @property
    def net_price(self):
        price = self.price - (self.price * self.discount / 100)
        return price

    @property
    def favorite_count(self):
        q = Favorite.objects.filter(shop_product=self)
        q = q.filter(favorite=True)
        return q.count()

    def get_absolute_url(self):
        return reverse("Shopproduct_detail", kwargs={"pk": self.pk})


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_favorite", on_delete=models.SET_NULL, null=True, blank=True)
    shop_product = models.ForeignKey(ShopProduct,related_name="shop_favorite",on_delete=models.CASCADE,)
    favorite = models.BooleanField(_("favorite"),default=False)

    class Meta:
        unique_together= [['user','shop_product']]
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("favorite_detail", kwargs={"pk": self.pk})


class ProductMeta(models.Model):
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE)
    label = models.CharField(_("Label"), max_length=50)
    value  = models.CharField(_("Value"), max_length=50)
    
    class Meta:
        verbose_name = _("ProductMeta")
        verbose_name_plural = _("ProductMetaes")

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("ProductMeta_detail", kwargs={"pk": self.pk})


class CategoryMeta(models.Model):
    category = models.ForeignKey("Category", verbose_name=_("Category"),related_name="category_meta", on_delete=models.CASCADE)
    label = models.CharField(_("Label"), max_length=50)

    class Meta:
        verbose_name = _("CategoryMeta")
        verbose_name_plural = _("CategoryMetas")

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse("CategoryMeta_detail", kwargs={"pk": self.pk})


class CategoryMetaValue(models.Model):
    label = models.ForeignKey("CategoryMeta", verbose_name=_("label"),related_name="label_meta" ,on_delete=models.CASCADE)
    value = models.CharField(_("value"), max_length=50)

    class Meta:
        verbose_name = _("CategoryMetaValue")
        verbose_name_plural = _("CategoryMetaValues")

    def __str__(self):
        return self.value

    def get_absolute_url(self):
        return reverse("CategoryMetaValue_detail", kwargs={"pk": self.pk})


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_like", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey("Product", verbose_name=_("Product"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("Like_detail", kwargs={"pk": self.pk})


class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', verbose_name=_(
        'Comment'),related_name="comment_like", on_delete=models.CASCADE)
    condition = models.BooleanField(_("Condition"), null=True, blank=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        unique_together= [['user','comment']]
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return str(self.condition) +" name:" +self.user.email +" comment:"+self.comment.text

    @property
    def get_condition(self):
        return self.condition
