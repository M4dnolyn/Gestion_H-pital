from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from .models import Consultation, Ordonnance
from personnes.serializers import PatientSerializer, PersonnelSerializer
from planning.serializers import RendezVousSerializer

class ConsultationSerializer(DynamicFieldsModelSerializer):
    patient_info = PatientSerializer(source='patient', read_only=True)
    medecin_info = PersonnelSerializer(source='medecin', read_only=True)
    rendezvous_info = RendezVousSerializer(source='rendezvous', read_only=True)
    
    class Meta:
        model = Consultation
        fields = '__all__'

class OrdonnanceSerializer(DynamicFieldsModelSerializer):
    consultation_info = ConsultationSerializer(source='consultation', read_only=True)
    
    class Meta:
        model = Ordonnance
        fields = '__all__'
