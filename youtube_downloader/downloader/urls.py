# downloader/urls.py
from django.urls import path
from .views import download_view

urlpatterns = [
    path('', download_view, name='download'),
]
