from django.core.exceptions import ValidationError
from django.forms import PasswordInput,EmailInput
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from .validators import validate_username, validate_password

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(
        label=_('repeat password'), widget=forms.PasswordInput, required=True)
    print('injaa form register to form ')

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
        help_texts = {'email': _('please enter a valid email'),
                      'password': _('enter a password')}
        labels = {
            "Email": "*Email",
            "password": "*Password"
        }
        widgets = {
            "Email":  EmailInput(attrs={'placeholder': 'ex:test', 'autocomplete': 'off'}),
            "password": PasswordInput(attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get("password2", None)
        print('----------------------------> password=', password)
        if password != password2:
            raise ValidationError(_("password don' match!"), code='invalid')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        print('----------------------------> avatar=', avatar)
        return avatar

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        print('----------------------------> username=', username)
        validate_username(username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        validate_password(password)
        return password
