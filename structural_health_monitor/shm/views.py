from django.shortcuts import render
from django.views.generic import TemplateView
from shm.models import Structure, EventLog


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from shm.models import SensorData
import datetime


class DashboardView(TemplateView):
    template_name = 'shm/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['structures'] = Structure.objects.all()
        context['latest_events'] = EventLog.objects.order_by('-timestamp')[:10]
        
        # Add sensor data for each structure
        for structure in context['structures']:
            structure.latest_data = structure.sensordata_set.order_by('-timestamp')[:5]
        
        return context
    

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
                'label': entry.get_sensor_type_display(),
                'data': [],
                'borderColor': entry.get_color(entry.sensor_type),
                'tension': 0.1
            }
        datasets[entry.sensor_type]['data'].append({
            'x': entry.timestamp.isoformat(),
            'y': entry.value
        })
    
    return JsonResponse({
        'datasets': list(datasets.values())
    })

def get_color(self, sensor_type):
    colors = {
        'vibration': 'rgb(75, 192, 192)',
        'strain': 'rgb(255, 99, 132)',
        'temperature': 'rgb(255, 159, 64)',
        'displacement': 'rgb(153, 102, 255)'
    }
    return colors.get(sensor_type, 'rgb(201, 203, 207)')