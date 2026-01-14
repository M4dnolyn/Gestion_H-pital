from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from .models import Prestation, Facture, Paiement, FacturePrestation
from personnes.serializers import PatientSerializer

class PrestationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Prestation
        fields = '__all__'

class FacturePrestationSerializer(DynamicFieldsModelSerializer):
    prestation_info = PrestationSerializer(source='prestation', read_only=True)
    montant_ligne = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = FacturePrestation
        fields = '__all__'
    
    def get_montant_ligne(self, obj):
        return obj.montant_ligne()

class FactureSerializer(DynamicFieldsModelSerializer):
    patient_info = PatientSerializer(source='patient', read_only=True)
    lignes = FacturePrestationSerializer(many=True, read_only=True)
    montant_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    statut_paiement_display = serializers.CharField(source='get_statut_paiement_display', read_only=True)
    
    class Meta:
        model = Facture
        fields = '__all__'
    
    def get_montant_total(self, obj):
        return sum(ligne.montant_ligne() for ligne in obj.lignes.all())

class PaiementSerializer(DynamicFieldsModelSerializer):
    facture_info = FactureSerializer(source='facture', read_only=True)
    
    class Meta:
        model = Paiement
        fields = '__all__'
