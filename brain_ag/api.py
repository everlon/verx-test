from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer, ProdutorRuralSerializer, CulturaPlantadaSerializer
from .models import ProdutorRural, CulturaPlantada


class ProdutorRuralViewSet(viewsets.ModelViewSet):
    queryset = ProdutorRural.objects.all()
    serializer_class = ProdutorRuralSerializer


class CulturaPlantadaViewSet(viewsets.ModelViewSet):
    queryset = CulturaPlantada.objects.all()
    serializer_class = CulturaPlantadaSerializer

