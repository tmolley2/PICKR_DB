# primers/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views # Import the entire views module, which is a cleaner approach

urlpatterns = [
    # Page views
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('api-docs/', views.api_docs, name='api_docs'),
    path('how-to-use/', views.how, name='how'),

    # Gene List page
    path('genes/', views.gene_list, name='gene_list'),

    # API endpoints
    # [FIXED] Using the correct view name 'PrimerListView' and removing the duplicate entry.
    path('api/primers/', views.PrimerListView.as_view(), name='primer-list'),
    
    # [FIXED] These are the other required API endpoints.
    path('api/gene-detail/<str:symbol>/', views.GeneDetailView.as_view(), name='gene-detail'),
    path('api/alias-lookup/<str:alias>/', views.AliasLookupView.as_view(), name='alias-lookup'),
    path('api/gene-list-for-species/', views.GeneListForSpeciesView.as_view(), name='gene-list-for-species'),

    # This is the old suggestions API. The new frontend doesn't use it, but we'll leave it for now.
    # You can delete this line later if you confirm it's no longer needed.
    path('api/gene-suggestions/', views.GeneSuggestionsAPIView.as_view(), name='gene-suggestions'),

    # Webscraping helpers
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml'), name='sitemap'),
]