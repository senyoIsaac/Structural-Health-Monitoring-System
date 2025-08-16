from django.db import models

# Create your models here.


class Structure(models.Model):
    STRUCTURE_TYPES = (
        ('bridge', 'Bridge'),
        ('building', 'Building'),
        ('tunnel', 'Tunnel'),
    )
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=STRUCTURE_TYPES)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    health_status = models.CharField(max_length=20, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def update_health_status(self):
        # Get latest sensor data
        latest_data = self.sensordata_set.order_by('-timestamp')[:5]
        critical_count = sum(1 for data in latest_data if data.is_critical())
        
        if critical_count >= 3:
            self.health_status = 'critical'
        elif critical_count >= 1:
            self.health_status = 'warning'
        else:
            self.health_status = 'normal'
        self.save()

class SensorData(models.Model):
    SENSOR_TYPES = (
        ('vibration', 'Vibration'),
        ('strain', 'Strain'),
        ('temperature', 'Temperature'),
        ('displacement', 'Displacement'),
    )
    
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def is_critical(self):
        thresholds = {
            'vibration': 10.0,
            'strain': 0.003,
            'temperature': 50.0,
            'displacement': 20.0
        }
        return abs(self.value) > thresholds.get(self.sensor_type, 0)