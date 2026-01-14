from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'medecin', 'date_rdv', 'heure_rdv', 'statut_rdv', 'motif_court')
    list_filter = ('statut_rdv', 'date_rdv', 'medecin__fonction')
    search_fields = ('patient__nom', 'patient__prenom', 'medecin__nom', 'motif')
    raw_id_fields = ('patient', 'medecin')
    date_hierarchy = 'date_rdv'
    list_editable = ('statut_rdv',)
    
    def motif_court(self, obj):
        return obj.motif[:50] + '...' if len(obj.motif) > 50 else obj.motif
    motif_court.short_description = 'Motif'
