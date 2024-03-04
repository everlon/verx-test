from django.db.models import Avg, Sum
from rest_framework import serializers

from django.contrib.auth.models import Group, User
from .models import ProdutorRural



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProdutorRuralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutorRural
        fields = (
            'id',
            'submitter',
            'cpf_cnpj',
            'nome_produtor',
            'nome_fazenda',
            'cidade',
            'estado',
            'area_total',
            'area_agricultavel',
            'area_vegetacao',
            'cultura'
        )
