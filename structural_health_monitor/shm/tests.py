from django.test import TestCase
from shm.models import Structure, SensorData

class StructureModelTest(TestCase):
    def setUp(self):
        self.structure = Structure.objects.create(
            name="Test Bridge",
            type="bridge",
            location="Test Location"
        )
    
    def test_health_status_update(self):
        # Create normal data
        for _ in range(5):
            SensorData.objects.create(
                structure=self.structure,
                sensor_type='vibration',
                value=1.0
            )
        
        self.structure.update_health_status()
        self.assertEqual(self.structure.health_status, 'normal')
        
        # Create warning data
        SensorData.objects.create(
            structure=self.structure,
            sensor_type='vibration',
            value=15.0  # Above threshold
        )
        self.structure.update_health_status()
        self.assertEqual(self.structure.health_status, 'warning')