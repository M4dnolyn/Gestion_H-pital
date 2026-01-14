from django.contrib import admin
from .models import Prestation, Facture, Paiement, FacturePrestation

class FacturePrestationInline(admin.TabularInline):
    model = FacturePrestation
    extra = 1
    autocomplete_fields = ['prestation']

@admin.register(Prestation)
class PrestationAdmin(admin.ModelAdmin):
    list_display = ('libelle_acte', 'tarif_unitaire')
    search_fields = ('libelle_acte',)
    list_editable = ('tarif_unitaire',)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date_facture', 'statut_paiement', 'montant_total')
    list_filter = ('statut_paiement', 'date_facture')
    search_fields = ('patient__nom', 'patient__prenom', 'id')
    inlines = [FacturePrestationInline]
    
    def montant_total(self, obj):
        return sum(ligne.montant_ligne() for ligne in obj.lignes.all())
    montant_total.short_description = 'Montant Total'

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'facture', 'date_paiement', 'montant_paye', 'mode_paiement')
    list_filter = ('mode_paiement', 'date_paiement')
    search_fields = ('facture__id', 'reference')

