from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import date
from .models import RendezVous
from .serializers import RendezVousSerializer

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut_rdv', 'medecin', 'patient']
    search_fields = ['patient__nom', 'patient__prenom', 'medecin__nom', 'motif']
    ordering_fields = ['date_rdv', 'heure_rdv']
    
    @action(detail=False, methods=['get'])
    def aujourdhui(self, request):
        """Rendez-vous du jour"""
        rdvs = RendezVous.objects.filter(date_rdv=date.today())
        serializer = self.get_serializer(rdvs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirmer(self, request, pk=None):
        """Confirmer un rendez-vous"""
        rdv = self.get_object()
        rdv.statut_rdv = 'Confirmé'
        rdv.save()
        serializer = self.get_serializer(rdv)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annuler un rendez-vous"""
        rdv = self.get_object()
        rdv.statut_rdv = 'Annulé'
        rdv.save()
        serializer = self.get_serializer(rdv)
        return Response(serializer.data)
