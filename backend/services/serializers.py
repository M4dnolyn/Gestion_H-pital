from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from .models import Service
from personnes.serializers import PersonnelSerializer

class ServiceSerializer(DynamicFieldsModelSerializer):
    responsable_info = PersonnelSerializer(source='responsable', read_only=True)
    personnel_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = '__all__'
    
    def get_personnel_count(self, obj):
        return obj.personnels.count()
