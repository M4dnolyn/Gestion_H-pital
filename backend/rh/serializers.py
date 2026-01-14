from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from .models import Conge, PersonnelService
from personnes.serializers import PersonnelSerializer
from services.serializers import ServiceSerializer

class PersonnelServiceSerializer(DynamicFieldsModelSerializer):
    personnel_info = PersonnelSerializer(source='personnel', read_only=True)
    service_info = ServiceSerializer(source='service', read_only=True)
    
    class Meta:
        model = PersonnelService
        fields = '__all__'

class CongeSerializer(DynamicFieldsModelSerializer):
    personnel_info = PersonnelSerializer(source='personnel', read_only=True)
    statut_display = serializers.CharField(source='get_statut_conge_display', read_only=True)
    
    class Meta:
        model = Conge
        fields = '__all__'
    
    def validate(self, data):
        # Validation: vérifier que date_fin > date_debut
        if 'date_debut' in data and 'date_fin' in data:
            if data['date_fin'] <= data['date_debut']:
                raise serializers.ValidationError(
                    "La date de fin doit être après la date de début."
                )
        return data
