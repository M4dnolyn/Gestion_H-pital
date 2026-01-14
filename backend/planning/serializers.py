from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from .models import RendezVous
from personnes.serializers import PatientSerializer, PersonnelSerializer

class RendezVousSerializer(DynamicFieldsModelSerializer):
    patient_info = PatientSerializer(source='patient', read_only=True)
    medecin_info = PersonnelSerializer(source='medecin', read_only=True)
    statut_display = serializers.CharField(source='get_statut_rdv_display', read_only=True)
    
    class Meta:
        model = RendezVous
        fields = '__all__'
        read_only_fields = ('statut_rdv',)
    
    def validate(self, data):
        # Validation: un patient ne peut pas avoir 2 RDV à la même heure
        if 'patient' in data and 'date_rdv' in data and 'heure_rdv' in data:
            conflits = RendezVous.objects.filter(
                patient=data['patient'],
                date_rdv=data['date_rdv'],
                heure_rdv=data['heure_rdv']
            )
            if self.instance:
                conflits = conflits.exclude(id=self.instance.id)
            if conflits.exists():
                raise serializers.ValidationError(
                    "Le patient a déjà un rendez-vous à cette heure."
                )
        return data
