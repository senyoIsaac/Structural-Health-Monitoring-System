# shm/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from .models import Structure, SensorData, EventLogs  # Import your models
import datetime

"""
# Temporary simple views to avoid import errors
def dashboard(request):
    return HttpResponse("""
'''<h1>Dashboard - Working!</h1>
    <p>The dashboard is working. Models will be imported after migrations.</p>
    <a href="/admin/">Admin Panel</a>'''
""")

def sensor_data_api(request, structure_id):
    return JsonResponse({"message": "API endpoint working", "structure_id": structure_id})

def structure_detail(request, structure_id):
    return HttpResponse(f"Structure detail for ID: {structure_id}")

def event_log(request):
    return HttpResponse("Event log will be here")   
    
"""

@login_required
def dashboard(request):
    structures = Structure.objects.all()  # Now Structure is defined
    latest_events = EventLogs.objects.order_by('-timestamp')[:10]
    
    # Add sensor data for each structure
    for structure in structures:
        structure.latest_data = SensorData.objects.filter(
            structure=structure
        ).order_by('-timestamp')[:5]
    
    return render(request, 'shm/dashboard.html', {
        'structures': structures,
        'latest_events': latest_events
    })

@login_required
def structure_detail(request, structure_id):
    structure = get_object_or_404(Structure, id=structure_id)  # Structure is defined
    sensor_data = SensorData.objects.filter(
        structure=structure
    ).order_by('-timestamp')[:50]
    
    return render(request, 'shm/structure_detail.html', {
        'structure': structure,
        'sensor_data': sensor_data
    })

@login_required
@require_GET
def sensor_data_api(request, structure_id):
    # Get data from last 24 hours
    time_threshold = datetime.datetime.now() - datetime.timedelta(hours=24)
    
    data = SensorData.objects.filter(
        structure_id=structure_id,
        timestamp__gte=time_threshold
    ).order_by('timestamp')
    
    # Format data for Chart.js
    datasets = {}
    for entry in data:
        if entry.sensor_type not in datasets:
            datasets[entry.sensor_type] = {
                'label': dict(SensorData.SENSOR_TYPES).get(entry.sensor_type, entry.sensor_type),
                'data': [],
                'borderColor': get_color(entry.sensor_type),
                'tension': 0.1
            }
        datasets[entry.sensor_type]['data'].append({
            'x': entry.timestamp.isoformat(),
            'y': entry.value
        })
    
    return JsonResponse({
        'datasets': list(datasets.values())
    })

@login_required
def event_log(request):
    events = EventLogs.objects.all().order_by('-timestamp')
    return render(request, 'shm/event_log.html', {'events': events})

# Helper function
def get_color(sensor_type):
    colors = {
        'vibration': 'rgb(75, 192, 192)',
        'strain': 'rgb(255, 99, 132)',
        'temperature': 'rgb(255, 159, 64)',
        'displacement': 'rgb(153, 102, 255)'
    }
    return colors.get(sensor_type, 'rgb(201, 203, 207)')