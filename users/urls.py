from django.urls import path

from .views import AlterarEmpresa

urlpatterns = [
    path('alterar-empresas/', AlterarEmpresa.as_view(), name='alterar-empresa')
]
