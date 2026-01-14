from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from datetime import datetime
from .models import Prestation, Facture, Paiement, FacturePrestation
from .serializers import PrestationSerializer, FactureSerializer, PaiementSerializer, FacturePrestationSerializer

class PrestationViewSet(viewsets.ModelViewSet):
    queryset = Prestation.objects.all()
    serializer_class = PrestationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['libelle_acte']

class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut_paiement', 'patient']
    search_fields = ['patient__nom', 'patient__prenom']
    ordering_fields = ['date_facture', 'statut_paiement']
    
    @action(detail=True, methods=['post'])
    def ajouter_prestation(self, request, pk=None):
        """Ajouter une prestation à une facture"""
        facture = self.get_object()
        prestation_id = request.data.get('prestation_id')
        quantite = request.data.get('quantite', 1)
        
        try:
            prestation = Prestation.objects.get(id=prestation_id)
        except Prestation.DoesNotExist:
            return Response({'detail': 'Prestation non trouvée'}, status=404)
        
        FacturePrestation.objects.create(
            facture=facture,
            prestation=prestation,
            qte=quantite,
            prix_unit=prestation.tarif_unitaire
        )
        
        serializer = self.get_serializer(facture)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques financières"""
        total_factures = Facture.objects.count()
        factures_payees = Facture.objects.filter(statut_paiement='Soldée').count()
        chiffre_affaires = Facture.objects.aggregate(
            total=Sum('lignes__prix_unit')
        )['total'] or 0
        
        return Response({
            'total_factures': total_factures,
            'factures_payees': factures_payees,
            'chiffre_affaires': chiffre_affaires,
        })

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['mode_paiement', 'facture']
    ordering_fields = ['date_paiement']

class FacturePrestationViewSet(viewsets.ModelViewSet):
    queryset = FacturePrestation.objects.all()
    serializer_class = FacturePrestationSerializer
    permission_classes = [permissions.IsAuthenticated]
