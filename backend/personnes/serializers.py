from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from .models import Patient, Personnel, ProcheAidant

class PatientSerializer(DynamicFieldsModelSerializer):
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('date_inscription',)
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_naissance.year - (
            (today.month, today.day) < (obj.date_naissance.month, obj.date_naissance.day)
        )

class PersonnelSerializer(DynamicFieldsModelSerializer):
    fonction_display = serializers.CharField(source='get_fonction_display', read_only=True)
    
    class Meta:
        model = Personnel
        fields = '__all__'

class ProcheAidantSerializer(DynamicFieldsModelSerializer):
    patients_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ProcheAidant
        fields = '__all__'
    
    def get_patients_info(self, obj):
        return [{'id': p.id, 'nom': p.nom, 'prenom': p.prenom} for p in obj.patients.all()]
