from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_basket", on_delete=models.SET_NULL, null=True, blank=True) 
    
    class Meta:
        verbose_name = _("Basket")
        verbose_name_plural = _("Baskets")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("Basket_detail", kwargs={"pk": self.pk})

class BasketItems(models.Model):
    basket = models.ForeignKey("Basket", verbose_name=_("Basket"), related_name="basket", on_delete=models.CASCADE)
    shop_product = models.ForeignKey("products.ShopProduct", verbose_name=_("Shop_product"),
                                     related_name="shop_product", on_delete=models.CASCADE)
    count = models.IntegerField(_("Count"),default=1)


    class Meta:
        verbose_name = _("BasketItem")
        verbose_name_plural = _("BasketItems")
        unique_together = ('basket', 'shop_product',)

    def __str__(self):
        return self.shop_product.product.name

    def get_absolute_url(self):
        return reverse("BasketItems_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_order", on_delete=models.SET_NULL, null=True, blank=True) 
    create_at = models.DateTimeField(_("Create_at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update_at"), auto_now=True)
    description = models.CharField(_("Description"), max_length=255)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

class OrderItems(models.Model):
    order = models.ForeignKey("Order", verbose_name=_("Order"), on_delete=models.CASCADE)
    shop_product = models.ForeignKey("products.ShopProduct", verbose_name=_("Shop_product_orderItems"), on_delete=models.CASCADE)
    count = models.IntegerField(_("Count"))
    price = models.IntegerField(_("Price"))

    class Meta:
        verbose_name = _("OrderItem")
        verbose_name_plural = _("OrdersItems")

    def total_price(self):
        return self.count * self.price

    def __str__(self):
        return str(self.count)

    def get_absolute_url(self):
        return reverse("OrderItems_detail", kwargs={"pk": self.pk})

class Payment(models.Model):
    order = models.ForeignKey("Order", verbose_name=_("Order"), on_delete=models.CASCADE)
    shop_product = models.ForeignKey("products.ShopProduct", verbose_name=_("Shop_product_orderItems"), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "User"),related_name="user_payment", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(_("Amount"))
    create_at = models.DateTimeField(_("Create_at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update_at"), auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return str(self.amount)

    def get_absolute_url(self):
        return reverse("Payment_detail", kwargs={"pk": self.pk})