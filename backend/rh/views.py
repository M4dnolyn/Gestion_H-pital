from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from .models import Conge, PersonnelService
from .serializers import CongeSerializer, PersonnelServiceSerializer

class CongeViewSet(viewsets.ModelViewSet):
    queryset = Conge.objects.all()
    serializer_class = CongeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type_conge', 'statut_conge', 'personnel']
    search_fields = ['personnel__nom', 'personnel__prenom']
    ordering_fields = ['date_debut', 'date_fin']
    
    @action(detail=True, methods=['post'])
    def approuver(self, request, pk=None):
        """Approuver un congé"""
        conge = self.get_object()
        conge.statut_conge = 'Approuvé'
        conge.save()
        serializer = self.get_serializer(conge)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rejeter(self, request, pk=None):
        """Rejeter un congé"""
        conge = self.get_object()
        conge.statut_conge = 'Rejeté'
        conge.save()
        serializer = self.get_serializer(conge)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def en_cours(self, request):
        """Congés en cours"""
        today = date.today()
        conges = Conge.objects.filter(
            date_debut__lte=today,
            date_fin__gte=today,
            statut_conge='Approuvé'
        )
        serializer = self.get_serializer(conges, many=True)
        return Response(serializer.data)

class PersonnelServiceViewSet(viewsets.ModelViewSet):
    queryset = PersonnelService.objects.all()
    serializer_class = PersonnelServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['service', 'personnel']
    search_fields = ['personnel__nom', 'personnel__prenom', 'service__nom_service']
