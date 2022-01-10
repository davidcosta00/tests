from django import forms
from django.contrib.auth import forms as auth_form

from .models import Empresas, User


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

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        if self.instance.empresa:
            grupo_empresarial = self.instance.empresa.grupo_empresarial
            empresa_query = Empresas.objects.filter(grupo_empresarial=grupo_empresarial)
            self.fields['empresa'].queryset = empresa_query
