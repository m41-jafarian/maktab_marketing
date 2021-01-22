from .models import Profile
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','avatar','address','phone_number','mobile_number')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')




