from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom_service', 'localisation', 'responsable', 'personnel_count')
    search_fields = ('nom_service', 'localisation', 'responsable__nom')
    list_filter = ('localisation',)
    raw_id_fields = ('responsable',)
    
    def personnel_count(self, obj):
        return obj.personnels.count()
    personnel_count.short_description = 'Nombre de personnel'
