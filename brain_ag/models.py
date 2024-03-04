from django.db import models
from django.contrib.auth.models import User


UF_CHOICES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)


class CulturaPlantada(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ['name',]
        verbose_name = 'Cultura plantada'
        verbose_name_plural = 'Culturas plantadas'

    def __str__(self):
        return self.name


class ProdutorRural(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    cpf_cnpj = models.CharField('CPF ou CNPJ', max_length=50, null=False, unique=True) 
    nome_produtor = models.CharField('Nome do produtor', max_length=150, null=False)
    nome_fazenda = models.CharField('Nome da fazenda', max_length=150, null=False)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2, choices=UF_CHOICES)
    area_total = models.DecimalField('Área total em hectares da fazenda', default=0, max_digits=12, decimal_places=0)
    area_agricultavel = models.DecimalField('Área agricultável em hectares', default=0, max_digits=12, decimal_places=0)
    area_vegetacao = models.DecimalField('Área de vegetação em hectares', default=0, max_digits=12, decimal_places=0)
    cultura = models.ManyToManyField(CulturaPlantada)

    class Meta:
        ordering = ['nome_produtor', 'nome_fazenda', 'estado', 'cidade']
        verbose_name = 'Nome do produtor'
        verbose_name_plural = 'Nomes dos produtores'

    def __str__(self):
        return self.nome_produtor + ' - ' + self.nome_fazenda
