# shm/admin.py
from django.contrib import admin
from .models import Structure

@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'health_status', 'manager']
    list_filter = ['type', 'health_status']