from django.views.generic import TemplateView
from users.models import User


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # recupera o contexto da página
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(email=self.request.user).first()
        if user:
            context['empresa_logada'] = user.empresa
        return context
