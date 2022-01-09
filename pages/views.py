from django.views.generic import TemplateView
from users.models import User

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # recupera o contexto da página
        context = super().get_context_data(**kwargs)
        context['empresa_logada'] = User.objects.get(email=self.request.user).empresa
        return context