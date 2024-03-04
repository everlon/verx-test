from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer, ProdutorRuralSerializer
from .models import ProdutorRural


class ProdutorRuralViewSet(viewsets.ModelViewSet):
    queryset = ProdutorRural.objects.all()
    serializer_class = ProdutorRuralSerializer
