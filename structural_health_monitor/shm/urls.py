# shm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('structures/<int:structure_id>/', views.structure_detail, name='structure_detail'),
    path('api/data/<int:structure_id>/', views.sensor_data_api, name='sensor_data_api'),
    path('events/', views.event_log, name='event_log'),
]

