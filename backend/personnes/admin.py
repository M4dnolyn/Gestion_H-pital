from django.contrib import admin
from .models import Patient, Personnel, ProcheAidant

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'groupe_sanguin', 'assurance')
    search_fields = ('nom', 'prenom', 'assurance')
    list_filter = ('sexe',)

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'fonction', 'specialite', 'statut')
    list_filter = ('fonction', 'statut')
    search_fields = ('nom', 'prenom', 'specialite')  # IMPORTANT pour autocomplete

@admin.register(ProcheAidant)
class ProcheAidantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'lien_parent', 'telephone', 'date_naissance')
    search_fields = ('nom', 'prenom', 'telephone')  # Ajouté
    filter_horizontal = ('patients',)
