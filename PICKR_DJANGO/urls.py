# PICK_DJANGO/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home and API are served from primers.urls
    path('', include('primers.urls')),
    path('', include('genes.urls')),
]
