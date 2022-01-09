from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from users.models import User

# Create your views here.

class AlterarEmpresa(UpdateView):
    model = User
    fields = ['empresa']
    template_name = 'form.html'
    success_url = reverse_lazy('account_signup')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(User, email=(self.request.user))
        return self.object

  

#class AlterarEmpresa(TemplateView):
#    template_name = 'form.html'
#
