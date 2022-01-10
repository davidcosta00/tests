from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class GrupoEmpresarial(TimeStampedModel):
    grupo_empresarial = models.CharField('Grupo Empresarial', max_length=50)

    def __str__(self):
        return self.grupo_empresarial

    class Meta:
        verbose_name = "Grupo Empresarial"
        verbose_name_plural = "Grupos Empresariais"


class Empresas(TimeStampedModel):
    razao_social = models.CharField('Razão Social', max_length=200)
    apelido = models.CharField('Apelido', max_length=50)
    cnpj_matriz = models.CharField('CNPJ Matriz', max_length=14, unique=True)
    grupo_empresarial = models.ForeignKey(
        GrupoEmpresarial,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return "{}--{}".format(self.apelido, self.cnpj_matriz)

    class Meta:
        verbose_name = "Empresas"
        verbose_name_plural = "Empresas"


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField('E-mail', max_length=254, unique=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)
    empresa = models.ForeignKey(
        Empresas,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    grupo_empresarial = models.ForeignKey(
        GrupoEmpresarial,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
