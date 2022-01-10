from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.forms import UserForm
from users.models import User


class AlterarEmpresa(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('account_signup')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, email=(self.request.user))
        return self.object
