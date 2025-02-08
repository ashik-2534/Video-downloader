# downloader/urls.py
from django.urls import path
from .views import download_view, download_status, task_status_json

urlpatterns = [
    path('', download_view, name='download'),
    path('status/<str:task_id>/', download_status, name='download_status'),
    path('task_status/<str:task_id>/', task_status_json, name='task_status_json'),
]
