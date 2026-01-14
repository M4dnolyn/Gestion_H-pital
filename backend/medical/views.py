from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Consultation, Ordonnance
from .serializers import ConsultationSerializer, OrdonnanceSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['medecin', 'patient']
    search_fields = ['patient__nom', 'patient__prenom', 'diagnostic']
    ordering_fields = ['date_consultation', 'heure_consultation']
    
    @action(detail=True, methods=['get'])
    def ordonnance(self, request, pk=None):
        """Obtenir l'ordonnance associée à une consultation"""
        consultation = self.get_object()
        try:
            ordonnance = consultation.ordonnance
            serializer = OrdonnanceSerializer(ordonnance)
            return Response(serializer.data)
        except Consultation.ordonnance.RelatedObjectDoesNotExist:
            return Response({'detail': 'Aucune ordonnance associée'}, status=404)

class OrdonnanceViewSet(viewsets.ModelViewSet):
    queryset = Ordonnance.objects.all()
    serializer_class = OrdonnanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['consultation__patient__nom', 'contenu_medical']
