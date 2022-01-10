from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from users.models import GrupoEmpresarial, Empresas, User

fake = Faker()


def create_groups():
    grupos = (
        'Grupo Um',
        'Grupo Dois',
        'Grupo Três',
    )

    for grupo in grupos:
        GrupoEmpresarial.objects.get_or_create(grupo_empresarial=grupo)


def create_companies():
    empresas = (
        ('Empresa 01', 'Empresa 01', '39670591031', 'Grupo Um'),
        ('Empresa 02', 'Empresa 02', '71502893045', 'Grupo Um'),
        ('Empresa 03', 'Empresa 03', '20703097032', 'Grupo Um'),
        ('Empresa 04', 'Empresa 04', '08276200044', 'Grupo Um'),
        ('Empresa 05', 'Empresa 05', '95686627070', 'Grupo Dois'),
        ('Empresa 06', 'Empresa 06', '55771152056', 'Grupo Dois'),
        ('Empresa 07', 'Empresa 07', '10374877025', 'Grupo Dois'),
        ('Empresa 08', 'Empresa 08', '97163481004', 'Grupo Dois'),
        ('Empresa 09', 'Empresa 09', '35133992009', 'Grupo Três'),
        ('Empresa 10', 'Empresa 10', '94507289092', 'Grupo Três'),
        ('Empresa 11', 'Empresa 11', '72116208033', 'Grupo Três'),
        ('Empresa 12', 'Empresa 12', '12203826045', 'Grupo Três'),
    )

    for empresa in empresas:
        grupo_empresarial = empresa[3]
        grupo = GrupoEmpresarial.objects.get(grupo_empresarial=grupo_empresarial)

        Empresas.objects.get_or_create(
            razao_social=empresa[0],
            apelido=empresa[1],
            cnpj_matriz=empresa[2],
            grupo_empresarial=grupo,
        )


def gen_email(first_name: str, last_name: str):
    first_name = slugify(first_name)
    last_name = slugify(last_name)
    email = f'{first_name}.{last_name}@email.com'
    return email


def get_user(empresa):
    nome = fake.first_name()
    sobrenome = fake.last_name()
    email = gen_email(nome, sobrenome)
    data = dict(
        email=email,
        username=email,
        nome=nome,
        sobrenome=sobrenome,
        empresa=empresa,
        # grupo_empresarial
    )
    return data


def create_users():
    User.objects.exclude(email='admin@email.com').delete()

    aux_list = []
    empresas = Empresas.objects.all()

    # Percorre todas as empresas.
    for empresa in empresas:
        # Adiciona 3 usuários para cada empresa.
        for _ in range(3):
            data = get_user(empresa)
            obj = User(**data)
            aux_list.append(obj)

    User.objects.bulk_create(aux_list)


class Command(BaseCommand):
    help = 'Create data.'

    def handle(self, *args, **options):
        create_groups()
        create_companies()
        create_users()
