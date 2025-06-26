from rest_framework import generics
from .models import PrimerPair
from .serializers import PrimerPairSerializer

class PrimerList(generics.ListAPIView):
    serializer_class = PrimerPairSerializer

    def get_queryset(self):
        gene = self.request.query_params.get('gene', '').upper()
        return PrimerPair.objects.filter(gene=gene)[:5]
