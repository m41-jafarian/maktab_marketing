from django.utils.safestring import mark_safe
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)
from products.models import Product,Brand

@hooks.register('insert_global_admin_css')
def customize_admin_colours():
    return mark_safe("""
<style>
:root {
  --main-bg-color: #343F4C;
  --primary-color: #1C86BA;
  --secondary-color: #36A3D9;
}
header {
  background-color: var(--main-bg-color);
}
a {
  color: var(--primary-color);
}
a:hover {
  color: var(--secondary-color);
}
.button,
header .button {
  background-color: var(--primary-color);
  border-color: var(--main-bg-color);
}
.button:hover,
.replace-file-input:hover button {
  background-color: var(--primary-color) !important;
}
.button-secondary {
  color: var(--main-bg-color);
}
</style>
""")

@hooks.register('construct_main_menu')
def hide_page_explorer_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'explorer']

@hooks.register('construct_homepage_summary_items')
def remove_pages_summary_item(request, summary_items):
    summary_items[:] = [i for i in summary_items if not isinstance(i, PagesSummaryItem)]

class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = 'Product'
    menu_icon = 'image'


class BrandAdmin(ModelAdmin):
    model = Brand
    menu_label = 'Brand'
    menu_icon = 'image'

modeladmin_register(ProductAdmin)
modeladmin_register(BrandAdmin)