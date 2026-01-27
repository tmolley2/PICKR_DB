# genes/urls.py
from django.urls import path
from .views import GeneDetailAPIView, AliasLookupAPIView # Import the new view

urlpatterns = [
    path('api/genes/<str:symbol>/', GeneDetailAPIView.as_view(), name='gene-detail'),
    # ADD THIS NEW URL PATTERN
    path('api/genes/alias/<str:alias_symbol>/', AliasLookupAPIView.as_view(), name='alias-lookup'),
]
