# primers/urls.py
from django.urls import path
from .views import home, contact, about, api_docs, PrimerPairListAPIView, GeneSuggestionsAPIView

urlpatterns = [
    # Page views
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('api-docs/', api_docs, name='api_docs'),

    # API endpoints
    path('api/primers/', PrimerPairListAPIView.as_view(), name='primer-list'),
    path('api/gene-suggestions/', GeneSuggestionsAPIView.as_view(), name='gene-suggestions'),
]
