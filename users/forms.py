from django import forms
from django.contrib.auth import forms as auth_form

from .models import User


class UserChangeForm(auth_form.UserChangeForm):

    class Meta(auth_form.UserChangeForm.Meta):
        model = User


class UserCreationForm(auth_form.UserCreationForm):

    class Meta(auth_form.UserCreationForm.Meta):
        model = User


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('empresa',)
