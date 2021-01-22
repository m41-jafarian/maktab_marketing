from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
User= get_user_model()
# Create your models here.
class SlideShow(models.Model):
    title = models.CharField(_("title"), max_length=50)
    subtitle = models.CharField(_("subtitle"), max_length=250)
    background = models.ImageField(_("background"), upload_to="site/slideshow", height_field=None, width_field=None, max_length=None)
    action_text = models.CharField(_("action text"), max_length=50)
    action_url = models.URLField(_("action url"), default='http://127.0.0.1:8000')

    class Meta:
        verbose_name = _("SlideShow")
        verbose_name_plural = _("SlideShows")

    def __str__(self):
        return self.title