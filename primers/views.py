# primers/views.py
from django.shortcuts import render
from django.db.models import F
from django.db.models.functions import Greatest, Least, Length, Abs, Coalesce
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from rest_framework import status


from .models import PrimerPair, GeneSymbol # Make sure both models are imported
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

def gene_list(request):
    """
    Fetches all unique gene names for each species and renders a paginated, filterable list.
    """
    active_species = request.GET.get('species', 'human')
    selected_letter = request.GET.get('letter', '')

    gene_list_qs = PrimerPair.objects.filter(species=active_species).values_list('gene', flat=True).distinct().order_by('gene')

    if selected_letter:
        gene_list_qs = gene_list_qs.filter(gene__istartswith=selected_letter)

    paginator = Paginator(gene_list_qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    context = {
        'page_obj': page_obj,
        'active_species': active_species,
        'alphabet': alphabet,
        'selected_letter': selected_letter,
    }
    return render(request, 'gene_list.html', context)


# API Views

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# [FIXED] Renamed from PrimerPairListAPIView to PrimerListView to match urls.py
class PrimerListView(generics.ListAPIView):
    """
    Returns primer pairs filtered by gene and other criteria.
    Supports filtering and sorting by species.
    """
    serializer_class = PrimerPairSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        species = self.request.query_params.get('species', 'human').lower()
        gene = self.request.query_params.get('gene', '').upper()

        if not gene:
            return PrimerPair.objects.none()

        queryset = PrimerPair.objects.filter(species=species, gene=gene)

        queryset = queryset.annotate(
            f_len=Length('f_sequence'),
            r_len=Length('r_sequence'),
            amplicon_max=Greatest(
                Coalesce('f_match_start', 0), Coalesce('r_match_start', 0),
                Coalesce('f_match_end', 0), Coalesce('r_match_end', 0)
            ),
            amplicon_min=Least(
                Coalesce('f_match_start', 0), Coalesce('r_match_start', 0),
                Coalesce('f_match_end', 0), Coalesce('r_match_end', 0)
            ),
            total_citations=F('f_pmcid_count') + F('r_pmcid_count'),
            delta_tm=Abs(F('f_Tm_C') - F('r_Tm_C'))
        ).annotate(
            amplicon_len=F('amplicon_max') - F('amplicon_min')
        )

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

# [ADDED] This view was missing but is required by your urls.py
class GeneDetailView(APIView):
    """
    Returns details for a single gene.
    """
    def get(self, request, symbol, *args, **kwargs):
        # This logic assumes you have a way to get a single gene's details.
        # You might need to adjust this based on your models.
        try:
            # Fetch the first PrimerPair entry as a representative for the gene details
            gene_data = PrimerPair.objects.filter(gene__iexact=symbol).first()
            if not gene_data:
                raise Http404
            # You might want a specific serializer for this
            response_data = {
                'symbol': gene_data.gene,
                'name': gene_data.gene_name,
                'alias_symbol': gene_data.alias_symbol,
                'gene_group': gene_data.gene_group,
            }
            return Response(response_data)
        except PrimerPair.DoesNotExist:
            raise Http404

# [ADDED] This view was missing but is required by your urls.py
class AliasLookupView(APIView):
    """
    Looks up a gene alias and returns the official symbol.
    """
    def get(self, request, alias, *args, **kwargs):
        try:
            # This logic assumes alias symbols are stored in a way that can be queried.
            # The query below looks for the alias in the `alias_symbol` field.
            gene = PrimerPair.objects.filter(alias_symbol__icontains=alias).first()
            if gene:
                return Response({'symbol': gene.gene})
            else:
                return Response({'symbol': None}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'An error occurred during alias lookup.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# [NEW] This is the new view for the client-side Trie search.
class GeneListForSpeciesView(APIView):
    """
    An API view to provide a flat list of gene symbols for a given species.
    This is optimized for the client-side Trie search.
    """
    def get(self, request, *args, **kwargs):
        species = request.query_params.get('species', None)
        if not species:
            return Response(
                {"error": "A 'species' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        gene_symbols = GeneSymbol.objects.filter(species=species.lower()).values_list('symbol', flat=True)
        return Response(list(gene_symbols))


# This view is now obsolete because the new Trie-based search on the client-side is faster.
# You can remove it if you are no longer using it.
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
