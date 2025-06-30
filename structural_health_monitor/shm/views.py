# shm/views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime

# Temporary simple views to avoid import errors
def dashboard(request):
    return HttpResponse("""
    <h1>Dashboard - Working!</h1>
    <p>The dashboard is working. Models will be imported after migrations.</p>
    <a href="/admin/">Admin Panel</a>
    """)

def sensor_data_api(request, structure_id):
    return JsonResponse({"message": "API endpoint working", "structure_id": structure_id})

def structure_detail(request, structure_id):
    return HttpResponse(f"Structure detail for ID: {structure_id}")

def event_log(request):
    return HttpResponse("Event log will be here")