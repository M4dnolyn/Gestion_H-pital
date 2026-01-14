from django.contrib import admin
from .models import Conge, PersonnelService

class PersonnelServiceInline(admin.TabularInline):
    model = PersonnelService
    extra = 1
    autocomplete_fields = ['personnel', 'service']

@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('id', 'personnel', 'type_conge', 'date_debut', 'date_fin', 'statut_conge')
    list_filter = ('type_conge', 'statut_conge', 'date_debut')
    search_fields = ('personnel__nom', 'personnel__prenom')
    raw_id_fields = ('personnel',)
    list_editable = ('statut_conge',)
    date_hierarchy = 'date_debut'

@admin.register(PersonnelService)
class PersonnelServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'personnel', 'service', 'date_affectation')
    list_filter = ('service', 'date_affectation')
    search_fields = ('personnel__nom', 'personnel__prenom', 'service__nom_service')
    autocomplete_fields = ['personnel', 'service']
