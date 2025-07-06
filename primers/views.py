# primers/views.py
from django.shortcuts import render
from django.db.models import F
# FIX: Import the Coalesce function
from django.db.models.functions import Greatest, Least, Length, Abs, Coalesce
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import PrimerPair
from .serializers import PrimerPairSerializer


# Main application views
def home(request):
    """Render the main search page."""
    return render(request, 'index.html')

def contact(request):
    """Render the contact page."""
    return render(request, 'contact.html')

def about(request):
    """Render the about page."""
    return render(request, 'about.html')

def api_docs(request):
    """Render the API documentation page."""
    return render(request, 'api.html')
    
def how(request):
    """Render the How-to page."""
    return render(request, 'how.html')

# API Views
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PrimerPairListAPIView(generics.ListAPIView):
    """
    Returns primer pairs filtered by gene and other criteria.
    Supports filtering and sorting by species.
    """
    serializer_class = PrimerPairSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Get species and gene from query parameters
        species = self.request.query_params.get('species', 'human').lower()
        gene = self.request.query_params.get('gene', '').upper()
        
        if not gene:
            return PrimerPair.objects.none()

        # The primary filter is now on both species and gene
        queryset = PrimerPair.objects.filter(species=species, gene=gene)

        # Annotate with calculated fields for filtering and sorting
        queryset = queryset.annotate(
            f_len=Length('f_sequence'),
            r_len=Length('r_sequence'),
            # FIX: Use Coalesce to handle potential NULL values in match fields, preventing crashes.
            # Coalesce will use the field value if it exists, otherwise it will use 0.
            amplicon_max=Greatest(
                Coalesce('f_match_start', 0), 
                Coalesce('r_match_start', 0), 
                Coalesce('f_match_end', 0), 
                Coalesce('r_match_end', 0)
            ),
            amplicon_min=Least(
                Coalesce('f_match_start', 0), 
                Coalesce('r_match_start', 0), 
                Coalesce('f_match_end', 0), 
                Coalesce('r_match_end', 0)
            ),
            total_citations=F('f_pmcid_count') + F('r_pmcid_count'),
            delta_tm=Abs(F('f_Tm_C') - F('r_Tm_C'))
        ).annotate(
            amplicon_len=F('amplicon_max') - F('amplicon_min')
        )

        # Apply filters from query params
        try:
            min_tm = self.request.query_params.get('min_tm')
            if min_tm:
                queryset = queryset.filter(f_Tm_C__gte=float(min_tm), r_Tm_C__gte=float(min_tm))
            
            max_tm = self.request.query_params.get('max_tm')
            if max_tm:
                queryset = queryset.filter(f_Tm_C__lte=float(max_tm), r_Tm_C__lte=float(max_tm))
            
            max_delta_tm = self.request.query_params.get('max_delta_tm')
            if max_delta_tm:
                queryset = queryset.filter(delta_tm__lte=float(max_delta_tm))

            min_gc = self.request.query_params.get('min_gc')
            if min_gc:
                queryset = queryset.filter(f_GC_pct__gte=float(min_gc), r_GC_pct__gte=float(min_gc))
            
            max_gc = self.request.query_params.get('max_gc')
            if max_gc:
                queryset = queryset.filter(f_GC_pct__lte=float(max_gc), r_GC_pct__lte=float(max_gc))
            
            min_len = self.request.query_params.get('min_len')
            if min_len:
                queryset = queryset.filter(f_len__gte=int(min_len), r_len__gte=int(min_len))
            
            max_len = self.request.query_params.get('max_len')
            if max_len:
                queryset = queryset.filter(f_len__lte=int(max_len), r_len__lte=int(max_len))
            
            min_amplicon = self.request.query_params.get('min_amplicon')
            if min_amplicon:
                queryset = queryset.filter(amplicon_len__gte=int(min_amplicon))
            
            max_amplicon = self.request.query_params.get('max_amplicon')
            if max_amplicon:
                queryset = queryset.filter(amplicon_len__lte=int(max_amplicon))
            
            min_citations = self.request.query_params.get('min_citations')
            if min_citations:
                queryset = queryset.filter(total_citations__gte=int(min_citations))
        except (ValueError, TypeError):
            pass

        # Apply sorting
        sort_by = self.request.query_params.get('sort_by')

        if sort_by == 'citations':
            return queryset.order_by('-total_citations', '-pickr_score')
        elif sort_by == 'amplicon':
            return queryset.order_by('amplicon_len', '-pickr_score')
        elif sort_by == 'delta_tm':
            return queryset.order_by('delta_tm', '-pickr_score')
        elif sort_by == 'shared_citations':
            return queryset.order_by('-pair_shared_pmcid_count', '-pickr_score')
        else:
            return queryset.order_by('-pickr_score')

class GeneSuggestionsAPIView(APIView):
    """Suggest related gene names when no exact match."""
    def get(self, request):
        species = request.query_params.get('species', 'human').lower()
        query = request.query_params.get('query', '').upper()
        
        if not query:
            return Response([])
            
        raw_genes = PrimerPair.objects.filter(
            species=species, 
            gene__icontains=query
        ).exclude(
            gene=query
        ).values_list('gene', flat=True)
        
        unique_genes = sorted(list(set(raw_genes)))[:10]
        return Response(unique_genes)
