from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from products.models import Comment

User = get_user_model()

class CommentForm(forms.ModelForm):
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