# genes/views.py
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gene
from .serializers import GeneDetailSerializer
from rest_framework import generics

class GeneDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve gene details by gene symbol.
    """
    queryset = Gene.objects.all()
    serializer_class = GeneDetailSerializer
    lookup_field = 'symbol'

# ADD THIS NEW VIEW
class AliasLookupAPIView(APIView):
    """
    Looks up a gene alias and returns the official symbol if a match is found.
    """
    def get(self, request, alias_symbol):
        query_symbol = alias_symbol.upper()

        # Find potential matches to reduce the number of records to process in Python
        potential_matches = Gene.objects.filter(
            Q(alias_symbol__icontains=query_symbol) | Q(prev_symbol__icontains=query_symbol)
        )

        # Iterate through the potential matches to find an exact, case-insensitive match
        for gene in potential_matches:
            aliases = (gene.alias_symbol or "").upper().split('|')
            prev_symbols = (gene.prev_symbol or "").upper().split('|')

            if query_symbol in aliases or query_symbol in prev_symbols:
                return Response({'symbol': gene.symbol}, status=status.HTTP_200_OK)

        # If no exact match is found
        return Response({'error': 'Alias not found'}, status=status.HTTP_404_NOT_FOUND)