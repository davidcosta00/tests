from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import Empresas, GrupoEmpresarial, User


class UserAdmin(BaseUserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        # Garante que o somente o super-usuário possa editar tais campos
        if not is_superuser:
            disabled_fields |= {
                'email',
                'nome',
                'password',
                'password1',
                'password2',
                'sobrenome',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return self.superuser_fieldsets
        else:
            return self.staff_fieldsets

# Campos do Super-Admin
    superuser_fieldsets = (
        (None, {'fields': ('email', 'password', 'nome', 'sobrenome', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        ('Configurações Empresa', {'fields': ('empresa', 'grupo_empresarial')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    # Campos dos admin
    staff_fieldsets = (
        (None, {'fields': ('email', 'nome', 'sobrenome', 'last_login')}),
        ('Configurações Empresa', {'fields': ('empresa', 'cargo')}),
    )

    list_display = ('email', 'nome', 'is_active', 'is_staff', 'last_login', 'get_grupo_empresarial', 'empresa')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'empresa')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    @admin.display(description='Grupo')
    def get_grupo_empresarial(self, obj):
        if obj.empresa:
            return obj.empresa.grupo_empresarial


@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'grupo_empresarial')
    search_fields = ('razao_social',)


admin.site.register(GrupoEmpresarial)
admin.site.register(User, UserAdmin)
