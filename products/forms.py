from django import forms
from django.contrib.admin import TabularInline
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from accounts.models import Shop
from products.models import Comment, Product, ShopProduct, Category, Brand, ProductMeta, CategoryMetaValue, CategoryMeta

User = get_user_model()

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'style': 'border-color: orange;width:100%;hieght:30%;padding:5px'}))
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'content': _('comment'),'rate':_('rate') }
        help_texts = {'content': _('Enter your comment here')}
        RATE_CHOICES = (
            ('', 'Select a rate'),
            ('1', '1'),  # First one is the value of select option and second is the displayed value in option
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        )
        widgets = {
            'content': forms.Textarea,'rate': forms.Select(choices=RATE_CHOICES, attrs={'class': 'form-control'}),
        }


class ProductCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'style': 'border-color: orange;width:100%;padding:5px'}))
    slug = forms.SlugField(widget=forms.TextInput(attrs={'style': 'border-color: orange;width:100%;padding:5px'}))
    detail = forms.CharField(widget=forms.Textarea(attrs={'style': 'border-color: orange;width:100%;padding:5px'}))

    class Meta:
        model = Product
        fields = ('name', 'slug', 'detail', 'category','brand', 'image')


class ShopProductCreateForm(forms.ModelForm):

    class Meta:
        model = ShopProduct
        fields = ('shop', 'product', 'price', 'quantity','discount')

    def __init__(self, *args, **kwargs):
        super(ShopProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['shop'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['product'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['quantity'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['price'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['discount'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','slug','detail','image','parent']

    def __init__(self, *args, **kwargs):
        super(CategoryCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['slug'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['detail'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['parent'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name','slug','detail','image','category']

    def __init__(self, *args, **kwargs):
        super(BrandCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['slug'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['detail'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['category'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})


class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['user','slug','name','image','discreption']

    def __init__(self, *args, **kwargs):
        super(ShopCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['slug'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['discreption'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['user'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})


class ProductMetaCreateForm(forms.ModelForm):
    class Meta:
        model = ProductMeta
        fields = ['product','label','value']


    def __init__(self, *args, **kwargs):
        super(ProductMetaCreateForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['label'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
        self.fields['value'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})


from django.forms import inlineformset_factory
class CategoryValueForm(forms.ModelForm):
    class Meta:
        model = CategoryMetaValue
        fields = ['label', 'value',]

class CategoryMetaFrom(forms.ModelForm):
    class Meta:
        model = CategoryMeta
        fields = ['category','label']

CategoryMetaValueSet = inlineformset_factory(CategoryMeta, CategoryMetaValue,fk_name='label',fields=['value',])

    # def __init__(self, *args, **kwargs):
    #     super(ProductMetaCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})
    #     self.fields['label'].widget.attrs.update({'class': 'shadow border border-info rounded w-100'})

