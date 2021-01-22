from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

def validate_password(password):
    if len(password) < 4:
        raise ValidationError(_('password too short!'), code='invalid   ')
    if len(password) > 150:
        raise ValidationError(_('password too long!'), code='invalid   ')
    return password

def validate_username(username):
    try:
        User.objects.get(username = username)
        raise ValidationError(_('this username is already exist!'),code='invalid')
    except User.DoesNotExist:
        pass
    return username