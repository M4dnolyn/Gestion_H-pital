from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Patient, Personnel, ProcheAidant
from .serializers import PatientSerializer, PersonnelSerializer, ProcheAidantSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sexe', 'groupe_sanguin', 'assurance']
    search_fields = ['nom', 'prenom', 'assurance', 'telephone']
    ordering_fields = ['nom', 'prenom', 'date_inscription']
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques sur les patients"""
        total = Patient.objects.count()
        by_sexe = {
            'M': Patient.objects.filter(sexe='M').count(),
            'F': Patient.objects.filter(sexe='F').count(),
        }
        return Response({
            'total_patients': total,
            'by_sexe': by_sexe,
        })

class PersonnelViewSet(viewsets.ModelViewSet):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['fonction', 'statut', 'service']
    search_fields = ['nom', 'prenom', 'specialite']

class ProcheAidantViewSet(viewsets.ModelViewSet):
    queryset = ProcheAidant.objects.all()
    serializer_class = ProcheAidantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'prenom', 'telephone']
