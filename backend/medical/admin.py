from django.contrib import admin
from .models import Consultation, Ordonnance

class OrdonnanceInline(admin.StackedInline):
    model = Ordonnance
    extra = 0
    max_num = 1

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'medecin', 'date_consultation', 'heure_consultation')
    list_filter = ('date_consultation', 'medecin__fonction')
    search_fields = ('patient__nom', 'patient__prenom', 'medecin__nom', 'diagnostic')
    raw_id_fields = ('patient', 'medecin', 'rendezvous')
    inlines = [OrdonnanceInline]
    date_hierarchy = 'date_consultation'

@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'consultation', 'date_prescription')
    search_fields = ('consultation__patient__nom', 'contenu_medical')
    raw_id_fields = ('consultation',)
