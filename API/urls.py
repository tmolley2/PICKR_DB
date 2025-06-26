# urls.py
from django.urls import path
from primers.views import PrimerList

urlpatterns = [
    path('api/primers/', PrimerList.as_view(), name='primer-list'),
]
